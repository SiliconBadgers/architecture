"use strict";
const fs = require("node:fs"),
  path = require("node:path"),
  crypto = require("node:crypto"),
  zlib = require("node:zlib");
const M = require("./model.cjs");
const modes = ["fixed", "microcode", "riscv-vector", "riscv-strip"];
const dir = __dirname;
const references = [];
for (const [op, n, rows, label] of [
  ["SOFT_MAX", 20736, 8, "20K-context attention row"],
  ["SOFT_MAX", 8192, 65536, "8K prefill attention layer"],
  ["RMS_NORM", 128, 16, "128-element head norm"],
  ["RMS_NORM", 2048, 1, "2048-element decode norm"],
  ["SWIGLU", 6144, 1, "6144-element decode gating"],
  ["SWIGLU", 6144, 8192, "8K prefill gating"],
]) {
  for (const localKiB of [0, 64, 512])
    for (const controller of modes) {
      const config = { ...M.defaults, localKiB };
      references.push({
        op,
        n,
        rows,
        label,
        controller,
        config,
        ...M.simulate(op, n, rows, controller, config),
      });
    }
}
const columns = [
  "op",
  "n",
  "rows",
  "engines",
  "lanes",
  "sramBpc",
  "localKiB",
  "specialPorts",
  "rvIssueCycles",
  "controllers",
  "overlapIssue",
  "fixed",
  "microcode",
  "riscvVector",
  "riscvStrip",
  "rvOverFixedPct",
  "stripOverFixedPct",
];
let csv = columns.join(",") + "\n",
  count = 0;
const ranges = { rvMin: Infinity, rvMax: 0, stripMin: Infinity, stripMax: 0 };
for (const op of ["SOFT_MAX", "RMS_NORM", "SWIGLU"])
  for (const n of [128, 2048, 6144, 8192, 20736])
    for (const engines of [1, 4, 8])
      for (const lanes of [16, 32, 64])
        for (const sramBpc of [16, 64, 256])
          for (const localKiB of [0, 16, 64, 512])
            for (const specialPorts of [1, 4, 16])
              for (const rvIssueCycles of [1, 4, 12])
                for (const controllers of [...new Set([1, engines])])
                  for (const overlapIssue of [false, true]) {
                    const c = {
                      engines,
                      lanes,
                      sramBpc,
                      localKiB,
                      specialPorts,
                      rvIssueCycles,
                      controllers,
                      overlapIssue,
                    };
                    const r = modes.map(
                        (x) => M.simulate(op, n, engines, x, c).cycles,
                      ),
                      rv = (r[2] / r[0] - 1) * 100,
                      strip = (r[3] / r[0] - 1) * 100;
                    csv +=
                      [
                        op,
                        n,
                        engines,
                        engines,
                        lanes,
                        sramBpc,
                        localKiB,
                        specialPorts,
                        rvIssueCycles,
                        controllers,
                        overlapIssue,
                        ...r,
                        rv,
                        strip,
                      ].join(",") + "\n";
                    count++;
                    ranges.rvMin = Math.min(ranges.rvMin, rv);
                    ranges.rvMax = Math.max(ranges.rvMax, rv);
                    ranges.stripMin = Math.min(ranges.stripMin, strip);
                    ranges.stripMax = Math.max(ranges.stripMax, strip);
                  }
fs.writeFileSync(path.join(dir, "sweep.csv.gz"), zlib.gzipSync(csv));
// Project only supported vector nodes into the prior analytical graph model.
const E = require("./inputs/engine.js"),
  G = require("./inputs/graph-data.js"),
  A = require("./inputs/architecture.cjs");
G.arch = A.architecture(require("./inputs/2B.json").text_config);
const projections = [];
for (const [prompt, context] of [
  [512, 2048],
  [8192, 20480],
]) {
  const c = {
    ...E.defaults(),
    precision: "w4a8",
    prompt,
    context,
    matrixCount: 2,
    rows: 32,
    cols: 32,
    vectorCount: 8,
    recurrentCount: 0,
    l1Banks: 64,
    dmaCount: 2,
  };
  const original = E.evaluate(G, c, true);
  for (const phase of ["prefill", "decode"])
    for (const localKiB of [0, 64, 512])
      for (const controller of modes) {
        const p = original[phase];
        let seconds = 0,
          replaced = 0,
          oldSeconds = 0,
          newSeconds = 0,
          issue = 0;
        const byOp = {};
        for (const row of p.rows) {
          if (!M.kernels[row.op]) {
            seconds += row.seconds;
            continue;
          }
          const sh = E.shapeOf(G.tensors[row.id], phase, c),
            n = sh[0],
            rows = row.elements / n;
          const v = M.simulate(row.op, n, rows, controller, {
            ...M.defaults,
            localKiB,
          });
          // Retain inherited HBM service unchanged; shared SRAM is explicitly modeled by the new kernel.
          const secondsNew =
            Math.max(
              (v.cycles - c.launchCycles) / (c.frequency * 1e6),
              row.hbm,
            ) +
            c.launchCycles / (c.frequency * 1e6);
          seconds += secondsNew;
          oldSeconds += row.seconds;
          newSeconds += secondsNew;
          replaced++;
          issue += v.issueCycles;
          const o = (byOp[row.op] ??= {
            nodes: 0,
            oldSeconds: 0,
            newSeconds: 0,
          });
          o.nodes++;
          o.oldSeconds += row.seconds;
          o.newSeconds += secondsNew;
        }
        projections.push({
          prompt,
          context,
          phase,
          localKiB,
          controller,
          seconds,
          originalSeconds: p.seconds,
          replacedNodes: replaced,
          totalNodes: p.rows.length,
          oldSelectedSeconds: oldSeconds,
          newSelectedSeconds: newSeconds,
          issueCycles: issue,
          byOp,
          inheritedChecksPass: original.valid,
        });
      }
}
const hashes = {};
for (const file of [
  "inputs/engine.js",
  "inputs/architecture.cjs",
  "inputs/graph-data.js",
  "inputs/2B.json",
  "model.cjs",
  "run.cjs",
])
  hashes[file] = crypto
    .createHash("sha256")
    .update(fs.readFileSync(path.join(dir, file)))
    .digest("hex");
const sensitivities = [];
for (const parameter of [
  "engines",
  "lanes",
  "sramBpc",
  "localKiB",
  "localBpcPerEngine",
  "specialPorts",
  "specialLatency",
  "reductionLatency",
  "rvIssueCycles",
  "controllers",
  "enginesPerCommand",
  "rvClockRatio",
]) {
  const values = {
    engines: [1, 2, 4, 8, 16],
    lanes: [8, 16, 32, 64, 128],
    sramBpc: [16, 32, 64, 128, 256, 512],
    localKiB: [0, 16, 64, 128, 256, 512],
    localBpcPerEngine: [16, 32, 64, 128, 256, 512],
    specialPorts: [1, 2, 4, 8, 16, 32],
    specialLatency: [4, 12, 32],
    reductionLatency: [1, 2, 4, 8],
    rvIssueCycles: [1, 2, 4, 8, 12, 24],
    controllers: [1, 2, 4, 8],
    enginesPerCommand: [1, 2, 4, 8],
    rvClockRatio: [0.25, 0.5, 1, 2],
  }[parameter];
  for (const value of values)
    for (const controller of modes)
      for (const [op, n, rows] of [
        ["SOFT_MAX", 20736, 8],
        ["RMS_NORM", 128, 16],
        ["SWIGLU", 6144, 8],
      ])
        sensitivities.push({
          parameter,
          value,
          controller,
          op,
          n,
          rows,
          ...M.simulate(op, n, rows, controller, {
            ...M.defaults,
            [parameter]: value,
          }),
        });
}
const result = {
  date: "2026-10-02",
  kind: "Analytical screening estimates; no RTL cycles or silicon measurements",
  defaults: M.defaults,
  sweepCases: count,
  modeEvaluations: count * 4,
  ranges,
  references,
  projections,
  sensitivities,
  sourceHashes: hashes,
  nodeVersion: process.version,
};
fs.writeFileSync(
  path.join(dir, "results.json"),
  JSON.stringify(result, null, 2),
);
console.log(
  JSON.stringify({ sweepCases: count, modeEvaluations: count * 4, ranges }),
);
console.table(
  references
    .filter((x) => x.config.localKiB === 64)
    .map((x) => ({
      kernel: x.label,
      mode: x.controller,
      us: x.us.toFixed(3),
      resident: x.resident,
    })),
);
console.table(
  projections
    .filter((x) => x.localKiB === 64)
    .map((x) => ({
      prompt: x.prompt,
      phase: x.phase,
      mode: x.controller,
      ms: (x.seconds * 1000).toFixed(3),
      selected: x.replacedNodes,
      all: x.totalNodes,
    })),
);
