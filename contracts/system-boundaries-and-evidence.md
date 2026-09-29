# System boundaries and design status

Status: architecture proposal for review, September 2026. This document defines the questions shared by Software, SoC, Control, Compute, and Memory. It does not freeze an accelerator ABI or choose a final compute partition.

## Workload and evidence

The initial workload is Qwen3.5-2B inference, including prompt processing and token-by-token generation. Its hybrid layers require dense matrix operations, attention with a KV cache, and recurrent and convolution state that persists across tokens. The [recorded llama.cpp experiment](https://github.com/SiliconBadgers/software/tree/main/experiments/llama-cpp/2026-09-22) and the [profiling extension under review](https://github.com/SiliconBadgers/software/pull/7) provide CPU timings, operation shapes, and graph observations. CPU time shares and graph structure identify work to investigate; they do not measure FPGA throughput, useful memory bandwidth, bank conflicts, or the area of a hardware partition.

The [shared accelerator diagram](../docs/accelerator-diagram.md) shows candidate engine functions and a command controller. Its four boxes are not a decision to build four independent arithmetic units. The [slide register and descriptor maps](../docs/register-maps.md) preserve a proposed ABI 0.1 baseline, not an implemented interface.

## Software-to-hardware path

The intended integration path is:

1. A model runtime builds operations and identifies tensor shape, format, layout, dependencies, and request state.
2. A lowering layer groups supported operations into device jobs and retains a CPU fallback for unsupported work.
3. A software or firmware submitter publishes device-visible descriptors and buffers, orders those writes, and rings a doorbell.
4. The accelerator validates the command, coordinates transfers and engines, and reports terminal completion with a matching sequence identifier.
5. The runtime observes completion before reusing buffers or advancing dependent work. Stateful commands also need explicit rules for sequence identity, token order, reset, replay, and invalidation after a fault.

The location of the command submitter is **open** ([architecture issue #7](https://github.com/SiliconBadgers/architecture/issues/7)). The current shared diagram depicts software or firmware on an existing CPU. A separate system proposal uses a small device-side RISC-V core between the application host and accelerator. In either option, the CPU executes instructions and the accelerator decodes commands; the controller is not a CPU. The selected placement changes address translation, cache visibility, interrupt routing, and the ownership boundary, so it must be decided in the shared architecture before either implementation is treated as final.

## Contracts to resolve together

| Contract | Questions that must agree across teams |
| --- | --- |
| Runtime to submitter | Which graph operations become jobs; supported shapes, formats and fallbacks; dependency and batching policy |
| Submitter to controller | Register and descriptor fields, address spaces, accepted-doorbell behavior, ordering, completion identity and acknowledgment |
| Controller to transfer and engines | Start acceptance, resource ownership, backpressure, terminal `done`, error propagation and buffer release |
| Compute and Memory | Tensor layout, byte strides, bank/port conflicts, accepted transfers, response ordering and output visibility |
| Persistent request state | KV cache, recurrent state, convolution history and token position; initialization, update order, checkpoint/replay and fault invalidation |
| Fault and reset | Stop new issue, drain accepted work, report a terminal outcome, and permit reset only after the agreed quiescence condition |

The [candidate boundary worksheet](accelerator-boundaries.md) records first checks that can use models and stubs. [Architecture issue #3](https://github.com/SiliconBadgers/architecture/issues/3) owns the proposed register/descriptor contract; [Control issue #2](https://github.com/SiliconBadgers/rtl-control/issues/2) owns the controller behavior; [Software issue #3](https://github.com/SiliconBadgers/software/issues/3) owns the workload-to-hardware boundary evidence. These are coupled reviews, not independent final interfaces.

## Decision status

One command in flight and a 128-byte descriptor are useful comparison baselines from the slide maps. They are not frozen. Shared versus dedicated matrix, vector, and recurrent arithmetic; local state storage; memory-bank organization; numerical formats; and supported model sizes need measured or modeled comparisons with stated assumptions. A profiler result may motivate such a comparison but should not be presented as a hardware result.

Before RTL interfaces are fixed, the teams need an agreed command acceptance/completion rule, a device-address and visibility model, persistent-state ownership, and a safe fault/reset rule. Array size, lane count, buffer depth, and unit count can remain parameters while those behaviors are specified.
