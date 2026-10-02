"use strict";
const assert = require("node:assert/strict"),
  fs = require("node:fs"),
  path = require("node:path"),
  zlib = require("node:zlib"),
  crypto = require("node:crypto"),
  M = require("./model.cjs");
let checks = 0;
function test(name, fn) {
  fn();
  checks++;
  console.log("PASS " + name);
}
test("zero dispatch cost equals fixed schedule", () => {
  for (const op of Object.keys(M.kernels))
    for (const n of [1, 31, 128, 8192]) {
      const a = M.simulate(op, n, 9, "fixed"),
        b = M.simulate(op, n, 9, "riscv-vector", { rvIssueCycles: 0 });
      assert.equal(a.cycles, b.cycles);
    }
});
test("controllers change time, not arithmetic or bytes", () => {
  for (const op of Object.keys(M.kernels))
    for (const localKiB of [0, 16, 512]) {
      const a = M.simulate(op, 8192, 17, "fixed", { localKiB });
      for (const mode of ["microcode", "riscv-vector", "riscv-strip"]) {
        const b = M.simulate(op, 8192, 17, mode, { localKiB });
        for (const key of ["sharedBytes", "localBytes", "computeCycles"])
          assert.equal(a[key], b[key]);
        assert(b.cycles >= a.cycles);
      }
    }
});
test("memory-only hand calculation for vector multiply", () => {
  const r = M.simulate("MUL", 32, 1, "fixed", {
    engines: 1,
    lanes: 32,
    sramBpc: 16,
    localKiB: 0,
  });
  assert.equal(r.sharedBytes, 32 * 4 * 3);
  assert.equal(r.cycles, 40 + 24);
});
test("eight head rows fill one wave; ninth requires a second", () => {
  const a = M.simulate("RMS_NORM", 128, 8, "fixed"),
    b = M.simulate("RMS_NORM", 128, 9, "fixed");
  assert(b.cycles > a.cycles);
});
test("local tiled elementwise traffic is only input/output on shared SRAM", () => {
  const r = M.simulate("SWIGLU", 6144, 8, "riscv-vector", { localKiB: 16 });
  assert(r.tiled);
  assert.equal(r.sharedBytes, 3 * 6144 * 8 * 4);
  assert(r.localBytes > r.sharedBytes);
});
test("softmax buffer threshold uses four FP32 row slots", () => {
  assert(!M.simulate("SOFT_MAX", 8192, 8, "fixed", { localKiB: 64 }).resident);
  assert(M.simulate("SOFT_MAX", 8192, 8, "fixed", { localKiB: 128 }).resident);
});
test("more issue controllers reduce dispatch, leave datapath unchanged", () => {
  const a = M.simulate("RMS_NORM", 128, 16, "riscv-vector", { controllers: 1 }),
    b = M.simulate("RMS_NORM", 128, 16, "riscv-vector", { controllers: 8 });
  assert(b.cycles < a.cycles);
  assert.equal(a.computeCycles, b.computeCycles);
});
test("issue overlap is an optimistic bound on same schedule", () => {
  for (const op of Object.keys(M.kernels)) {
    const a = M.simulate(op, 2048, 16, "riscv-strip"),
      b = M.simulate(op, 2048, 16, "riscv-strip", { overlapIssue: true });
    assert(b.cycles <= a.cycles);
  }
});
test("special-function throughput is not pipeline latency", () => {
  const a = M.simulate("SILU", 6144, 8, "fixed", { specialPorts: 1 }),
    b = M.simulate("SILU", 6144, 8, "fixed", { specialPorts: 16 });
  assert(b.cycles < a.cycles);
});
test("batched row issue amortizes dispatch without changing math or bytes", () => {
  const a = M.simulate("RMS_NORM", 128, 16, "riscv-vector"),
    b = M.simulate("RMS_NORM", 128, 16, "riscv-vector", {
      enginesPerCommand: 8,
    });
  assert(b.cycles < a.cycles);
  for (const k of ["sharedBytes", "localBytes", "computeCycles"])
    assert.equal(a[k], b[k]);
  assert.equal(
    b.cycles,
    M.simulate("RMS_NORM", 128, 16, "riscv-vector", { controllers: 8 }).cycles,
  );
});
test("selected results finite and projection node counts valid", () => {
  const r = require("./results.json");
  for (const x of [...r.references, ...r.sensitivities])
    assert(Number.isFinite(x.cycles) && x.cycles > 0);
  for (const p of r.projections) {
    assert(p.seconds > 0);
    assert(p.replacedNodes <= p.totalNodes);
  }
});
test("complete CSV coverage, controller lower bound, and input hashes", () => {
  const result = require("./results.json");
  const csv = zlib
    .gunzipSync(fs.readFileSync(path.join(__dirname, "sweep.csv.gz")))
    .toString()
    .trim()
    .split("\n");
  assert.equal(csv.length - 1, result.sweepCases);
  const header = csv.shift().split(",");
  for (const line of csv) {
    const row = Object.fromEntries(
      line.split(",").map((value, i) => [header[i], value]),
    );
    const values = ["fixed", "microcode", "riscvVector", "riscvStrip"].map(
      (key) => Number(row[key]),
    );
    for (const value of values) assert(Number.isFinite(value) && value > 0);
    for (const value of values.slice(1)) assert(value >= values[0]);
  }
  for (const [file, expected] of Object.entries(result.sourceHashes)) {
    assert.equal(
      crypto
        .createHash("sha256")
        .update(fs.readFileSync(path.join(__dirname, file)))
        .digest("hex"),
      expected,
      file,
    );
  }
});
console.log(
  `${checks} checks passed. These validate model accounting, not hardware performance.`,
);
