// Analytical cycle accounting, not an RTL simulator. See README.md.
"use strict";
const ceil = Math.ceil;
const defaults = {
  engines: 8,
  lanes: 32,
  sramBpc: 256,
  localKiB: 64,
  localBpcPerEngine: 64,
  specialPorts: 4,
  specialLatency: 12,
  reductionLatency: 4,
  frequencyMHz: 300,
  controllers: 1,
  enginesPerCommand: 1,
  rvIssueCycles: 4,
  rvClockRatio: 1,
  launchCycles: 40,
  overlapIssue: false,
};
// Stages: [arithmetic type, vector reads, vector writes]. Constants stay in scalar registers.
const kernels = {
  SOFT_MAX: {
    inputs: 2,
    slots: 4,
    stages: [
      ["alu", 2, 1],
      ["reduce", 1, 0],
      ["alu", 1, 1],
      ["special", 1, 1],
      ["reduce", 1, 0],
      ["scalar", 0, 0],
      ["alu", 1, 1],
    ],
  },
  RMS_NORM: {
    inputs: 1,
    slots: 3,
    stages: [
      ["alu", 1, 1],
      ["reduce", 1, 0],
      ["scalar", 0, 0],
      ["alu", 1, 1],
    ],
  },
  SILU: {
    inputs: 1,
    slots: 3,
    stages: [
      ["alu", 1, 1],
      ["special", 1, 1],
      ["alu", 1, 1],
      ["special", 1, 1],
      ["alu", 2, 1],
    ],
  },
  SWIGLU: {
    inputs: 2,
    slots: 4,
    stages: [
      ["alu", 1, 1],
      ["special", 1, 1],
      ["alu", 1, 1],
      ["special", 1, 1],
      ["alu", 2, 1],
      ["alu", 2, 1],
    ],
  },
  SIGMOID: {
    inputs: 1,
    slots: 2,
    stages: [
      ["alu", 1, 1],
      ["special", 1, 1],
      ["alu", 1, 1],
      ["special", 1, 1],
    ],
  },
  SOFTPLUS: {
    inputs: 1,
    slots: 2,
    stages: [
      ["special", 1, 1],
      ["alu", 1, 1],
      ["special", 1, 1],
    ],
  },
  MUL: { inputs: 2, slots: 3, stages: [["alu", 2, 1]] },
  ADD: { inputs: 2, slots: 3, stages: [["alu", 2, 1]] },
  SCALE: { inputs: 1, slots: 2, stages: [["alu", 1, 1]] },
};
function simulate(op, n, rows, controller, overrides = {}) {
  const c = { ...defaults, ...overrides },
    k = kernels[op];
  if (
    !k ||
    !Number.isInteger(n) ||
    n < 1 ||
    !Number.isInteger(rows) ||
    rows < 1
  )
    throw Error("Invalid kernel/shape");
  for (const x of [
    "engines",
    "lanes",
    "sramBpc",
    "localBpcPerEngine",
    "specialPorts",
    "rvClockRatio",
    "controllers",
  ])
    if (!(c[x] > 0)) throw Error("Invalid " + x);
  const resident = k.slots * n * 4 <= c.localKiB * 1024; // FP32 scratch, all controllers have identical storage.
  // Elementwise kernels can reuse a small tile buffer; reductions require separate row passes.
  const tileable = !["SOFT_MAX", "RMS_NORM"].includes(op);
  const tileN =
    Math.floor((c.localKiB * 1024) / (k.slots * 4 * c.lanes)) * c.lanes;
  if (tileable && !resident && tileN >= c.lanes) {
    const chunks = Math.floor(n / tileN),
      tail = n % tileN;
    const pieces = [];
    if (chunks) pieces.push([chunks, simulate(op, tileN, rows, controller, c)]);
    if (tail) pieces.push([1, simulate(op, tail, rows, controller, c)]);
    const r = {
      cycles: c.launchCycles,
      sharedBytes: 0,
      localBytes: 0,
      issueCycles: 0,
      computeCycles: 0,
      memoryCycles: 0,
    };
    for (const [count, p] of pieces) {
      r.cycles += count * (p.cycles - c.launchCycles);
      for (const key of [
        "sharedBytes",
        "localBytes",
        "issueCycles",
        "computeCycles",
        "memoryCycles",
      ])
        r[key] += count * p[key];
    }
    return {
      ...r,
      us: r.cycles / c.frequencyMHz,
      resident: true,
      tiled: true,
      scratchBytes: tileN * k.slots * 4,
      allocatedScratchBytes: c.localKiB * 1024 * c.engines,
    };
  }
  let total = c.launchCycles,
    issue = 0,
    compute = 0,
    memory = 0,
    sharedBytes = 0,
    localBytes = 0;
  function wave(active, multiplicity) {
    let t = 0,
      ct = 0,
      it = 0,
      mt = 0,
      sb = 0,
      lb = 0;
    // A batched command requires per-engine address generation and identical row operations.
    const chunks = ceil(n / c.lanes),
      groups = ceil(
        ceil(active / c.enginesPerCommand) / Math.min(active, c.controllers),
      );
    if (resident) {
      sb = (k.inputs + 1) * n * 4 * active;
      t += sb / c.sramBpc;
      mt += sb / c.sramBpc;
    }
    for (const [type, reads, writes] of k.stages) {
      const data = (reads + writes) * n * 4 * active;
      const mem = data / (resident ? c.localBpcPerEngine * active : c.sramBpc);
      if (resident) lb += data;
      else sb += data;
      let arithmetic =
        type === "alu"
          ? chunks + 3
          : type === "special"
            ? ceil(n / Math.min(c.specialPorts, c.lanes)) + c.specialLatency
            : type === "reduce"
              ? chunks * c.reductionLatency +
                ceil(Math.log2(c.lanes)) +
                c.reductionLatency
              : c.specialLatency;
      // Long instructions address an entire row; strip instructions address one lane-width chunk.
      let dispatch =
        controller === "fixed"
          ? 0
          : controller === "microcode"
            ? 2 * groups
            : controller === "riscv-vector"
              ? (c.rvIssueCycles * groups) / c.rvClockRatio
              : controller === "riscv-strip"
                ? (c.rvIssueCycles *
                    groups *
                    (type === "scalar" ? 1 : chunks)) /
                  c.rvClockRatio
                : NaN;
      if (!Number.isFinite(dispatch)) throw Error("Unknown controller");
      const service = Math.max(arithmetic, mem);
      t += c.overlapIssue ? Math.max(service, dispatch) : service + dispatch;
      ct += arithmetic;
      it += dispatch;
      mt += mem;
    }
    total += multiplicity * t;
    compute += multiplicity * ct;
    issue += multiplicity * it;
    memory += multiplicity * mt;
    sharedBytes += multiplicity * sb;
    localBytes += multiplicity * lb;
  }
  const full = Math.floor(rows / c.engines),
    tail = rows % c.engines;
  if (full) wave(c.engines, full);
  if (tail) wave(tail, 1);
  return {
    cycles: total,
    us: total / c.frequencyMHz,
    resident,
    sharedBytes,
    localBytes,
    issueCycles: issue,
    computeCycles: compute,
    memoryCycles: memory,
    scratchBytes: k.slots * n * 4,
    allocatedScratchBytes: c.localKiB * 1024 * c.engines,
  };
}
module.exports = { defaults, kernels, simulate };
