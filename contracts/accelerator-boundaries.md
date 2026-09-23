# Candidate accelerator boundaries

Status: design worksheet, not an approved ABI. The existing `mac-v0.json` is the
contract for the small MAC example only. No signal widths, descriptor offsets,
queue depths or numeric formats below are frozen.

| Boundary | Producer / consumer | Specify together | First check without complete RTL |
|---|---|---|---|
| Command submission | Software/SoC → Control | Operation, dimensions, buffer descriptors, sequence ID, validation and acceptance | Feed valid/invalid synthetic commands to a model; rejected commands must not modify state |
| Engine command/status | Control ↔ Compute | Acceptance, input readiness, completion meaning, error propagation, output ownership | Variable-latency engine stub with backpressure and injected errors |
| Buffer access | Compute ↔ Memory | Address units, layout/strides, alignment, masks, ordering, ports and arbitration | Competing accesses and tail tiles against a reference memory model |
| Transfer | Memory ↔ SoC/platform | Accepted requests, response identity, ordering, outstanding count, visibility | Stall responses and check that buffers cannot be reused early |
| Request state | Software/Control/Compute/Memory | KV/recurrent/history ownership, initialization, sequence isolation and invalidation after faults | Prefill, multiple decode steps, reset/reuse and interleaved request IDs in models |
| Completion | Control/SoC → Software | When output writes are visible, status/error, IRQ and acknowledgment | Delay a write response beyond arithmetic completion; completion must wait for the defined visibility point |
| Quiescence/reset | All hardware blocks | Stop new requests, drain accepted work, terminal state and allowed reset | Inject faults with outstanding traffic; a timeout alone must not free live buffers |

## Initial comparisons

Begin with one command in flight as a simple model, then compare coarse grouped
commands and controlled overlap. Keep latencies and queue sizes adjustable.
Do not allocate independent engines just because the diagram has separate boxes.

For each proposed interface, record: producer, consumer, data/units, acceptance
condition, completion condition, resource owner, backpressure behavior, errors,
reset behavior and a runnable/example trace. Signal-level choices follow that
behavioral agreement. Publish drafts early so other teams can build stubs.

## Open decisions

| Decision | Evidence needed | Participants |
|---|---|---|
| Shared versus dedicated arithmetic | Shape utilization, data movement, state/control cost and implementation estimates | Compute 1/2, Software, Memory, Physical Design |
| Numerical policy per tensor/state | Kernel comparisons and task-quality evidence; storage/arithmetic cost | Software, Verification, Compute, Architecture |
| Local storage and bank/port organization | Liveness, concurrent accesses and available memory macros | Memory, Compute, Physical Design |
| Command granularity | Dispatch/transfer overhead and dependency schedules | Control, SoC, Software |
| Recovery semantics | Which partial writes/state updates can be detected or invalidated | Control, Memory, Compute, Verification, Software |
| Target envelope | Available platform/tool/library constraints and workload objective | Architecture, SoC, Physical Design, all affected teams |

Use [decision-template.md](../decisions/decision-template.md) to record a choice
when enough evidence exists. Unresolved choices remain explicit parameters and
do not block unrelated investigations.
