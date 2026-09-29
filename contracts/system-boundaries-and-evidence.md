# System boundaries and design status

Status: architecture proposal for review, September 2026. This document defines the questions shared by Software, SoC, Control, Compute, and Memory. It does not freeze an accelerator ABI or choose a final compute partition.

## Workload and evidence

The initial workload is Qwen3.5-2B inference, including prompt processing and token-by-token generation. Its hybrid layers require dense matrix operations, attention with a KV cache, and recurrent and convolution state that persists across tokens. The [recorded llama.cpp experiment](https://github.com/SiliconBadgers/software/tree/main/experiments/llama-cpp/2026-09-22) and the [profiling extension under review](https://github.com/SiliconBadgers/software/pull/7) provide CPU timings, operation shapes, and graph observations. CPU time shares and graph structure identify work to investigate; they do not measure FPGA throughput, useful memory bandwidth, bank conflicts, or the area of a hardware partition.

The [shared accelerator diagram](../docs/accelerator-diagram.md) shows candidate engine functions and a command controller. Its four boxes are not a decision to build four independent arithmetic units. The [slide register and descriptor maps](../docs/register-maps.md) preserve a proposed ABI 0.1 baseline, not an implemented interface.

## Software-to-hardware path

The intended integration path is:

1. A model runtime builds operations and identifies tensor shape, format, layout, dependencies, and request state.
2. A lowering layer groups supported operations into device jobs and retains a CPU fallback for unsupported work.
3. Device-side RISC-V firmware publishes device-visible descriptors and buffers, orders those writes, and rings a doorbell.
4. The accelerator validates the command, coordinates transfers and engines, and reports terminal completion with a matching sequence identifier.
5. The runtime observes completion before reusing buffers or advancing dependent work. Stateful commands also need explicit rules for sequence identity, token order, reset, replay, and invalidation after a fault.

The working system design retains a small device-side RISC-V core between the application host and accelerator. The CPU executes firmware instructions; the accelerator controller independently decodes commands. [Architecture issue #7](https://github.com/SiliconBadgers/architecture/issues/7) tracks the **open split of graph decomposition and sequencing** between host and firmware, along with command granularity and the exact address, visibility, and interrupt contracts. The earlier shared diagram depicted an existing CPU as the sole submitter; this proposal updates that boundary without selecting a core implementation or final ABI.

## Contracts to resolve together

| Contract | Questions that must agree across teams |
| --- | --- |
| Host runtime to RISC-V firmware | Which graph operations become jobs; supported shapes, formats and fallbacks; dependency and batching policy |
| RISC-V firmware to controller | Register and descriptor fields, address spaces, accepted-doorbell behavior, ordering, completion identity and acknowledgment |
| Controller to transfer and engines | Start acceptance, resource ownership, backpressure, terminal `done`, error propagation and buffer release |
| Compute and Memory | Tensor layout, byte strides, bank/port conflicts, accepted transfers, response ordering and output visibility |
| Persistent request state | KV cache, recurrent state, convolution history and token position; initialization, update order, checkpoint/replay and fault invalidation |
| Fault and reset | Stop new issue, drain accepted work, report a terminal outcome, and permit reset only after the agreed quiescence condition |

The [candidate boundary worksheet](accelerator-boundaries.md) records first checks that can use models and stubs. [Architecture issue #3](https://github.com/SiliconBadgers/architecture/issues/3) owns the proposed register/descriptor contract; [Control issue #2](https://github.com/SiliconBadgers/rtl-control/issues/2) owns the controller behavior; [Software issue #3](https://github.com/SiliconBadgers/software/issues/3) owns the workload-to-hardware boundary evidence. These are coupled reviews, not independent final interfaces.

## Decision status

| Topic | Current status | What remains to be established |
| --- | --- | --- |
| Device-side RISC-V | Retained in the working system design | Host/firmware decomposition split, core implementation and firmware interface ([issue #7](https://github.com/SiliconBadgers/architecture/issues/7)) |
| Matrix and vector functions | Distinct functions in the initial design | Array/lane sizes, reuse and scheduling for prefill and one-token decode; dedicated attention or recurrence arithmetic must earn its cost |
| Compute-unit exchange | Shared SRAM path in the initial design; no separate compute-to-compute fabric | Useful bandwidth, bank/port conflicts and whether another path helps on the chosen target |
| Persistent state | KV, recurrent and convolution state must be maintained in request/token order | Local storage, spill policy, initialization, replay and fault invalidation |
| Numerical formats | Open; parameterized INT4/INT8 RTL may start | FP4 versus integer weights, activation/accumulator/state precision, conversion and model-quality effects |
| Command ABI | One command in flight and a 128-byte descriptor are comparison baselines | Acceptance, fields, address and visibility rules, error codes, reset and useful command granularity ([issue #3](https://github.com/SiliconBadgers/architecture/issues/3)) |
| FPGA and small ASIC | Separate target constraints; a representative-block tape-out is a proposal | Area, memory macros, I/O, packaging, clocking and which block could be tested usefully |

The next Software model should include dependent operation chains and stalls, joint compute/memory sweeps, prefill and decode, and local-memory and HBM working sets. CPU traces and preliminary model estimates are inputs to these comparisons, not measured FPGA performance. Memory can specify HBM-to-SRAM transfers and prefetching while its SRAM-to-compute interface is refined with Compute. Verification can develop models and fault/backpressure tests before every datapath parameter is final.

Before RTL interfaces are fixed, the teams need an agreed command acceptance/completion rule, a device-address and visibility model, persistent-state ownership, and a safe fault/reset rule. Array size, lane count, buffer depth, and unit count can remain parameters while those behaviors are specified.
