# Architecture starting material

September 22, 2026. Initial investigations for team discussion; no personal assignments or deadlines.

## Shared starting points

- [Editable architecture diagram](https://github.com/SiliconBadgers/architecture/blob/main/docs/accelerator-diagram.md) and [candidate boundaries](https://github.com/SiliconBadgers/architecture/blob/main/contracts/accelerator-boundaries.md).
- [Workload cases and source shapes](https://github.com/SiliconBadgers/architecture/blob/main/docs/workload-cases.md).
- [Measured llama.cpp report](https://github.com/SiliconBadgers/software/blob/main/experiments/llama-cpp/2026-09-22/REPORT.md) and [reproduction procedure](https://github.com/SiliconBadgers/software/blob/main/experiments/llama-cpp/2026-09-22/README.md).
- [Parallel team investigations](https://github.com/SiliconBadgers/planning/blob/main/docs/team-start.md).

The diagram and engine split are proposals. Start from available shapes and
reference cases now; use explicit parameters or stubs where decisions remain
open. Software's broader profiling study is not a prerequisite. Preserve the
source revision, assumptions, commands and limits of each result. Members and
leads can choose a different investigation that resolves a relevant uncertainty.


## First useful output

Compare at least two candidate partitions using the same workload cases: shared
matrix/vector arithmetic with local state controllers versus more dedicated
functional engines. Record operation coverage, intermediate/state ownership,
data movement, command boundaries and the evidence needed to choose. Use the
[decision template](../decisions/decision-template.md); the first output is a
reviewable comparison, not a frozen block count.

## Work that can start now

1. Review the [Mermaid hierarchy](accelerator-diagram.md) against the [boundary worksheet](../contracts/accelerator-boundaries.md).
2. Choose explicit optimization cases: single-sequence decode latency and prefill throughput should be compared separately. Record the target platform as a parameter until agreed.
3. Reconcile Compute's resource demand, Memory's traffic/ports, Control's dispatch cost and Physical Design's feasible widths/area. Keep numerical policy tied to Software/Verification evidence.
4. Update only the decisions affected by new evidence. Keep first-chip scope separate from the F2 study.

## Ready for a joint review when

Each alternative has a diagram, workload assumptions, state/buffer ownership,
quantitative cost estimates with units, limitations and a next discriminating
experiment. Nobody should infer area allocation from CPU timing percentages.
The existing `contracts/mac-v0.json` remains a small example, not the accelerator
contract. Run `make test` if changing that example's contract.
