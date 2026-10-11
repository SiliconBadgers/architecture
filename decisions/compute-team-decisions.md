# Compute team decisions

Status: accepted initial design decisions, with unresolved details identified below.
Decision dates: October 3 and October 10, 2026. Participants: Compute, with
Controller and Verification coordination.

## Context and objective

This record defines the compute direction agreed for the initial Qwen3.5-2B
accelerator implementation. It draws on the [October 3 compute meeting][oct3]
and [October 10 compute meeting][oct10]. The [September 28 technical sync][sep28]
provides the earlier agreement on shared SRAM and device-side RISC-V control.

Use the [central accelerator diagram](../docs/accelerator-diagram.md) for the
system view. Its attention and DeltaNet boxes describe functions to support;
they do not require separate arithmetic engines. This record captures team
agreements, not a completed accelerator or a frozen software-visible ABI.

## Decision and consequences

### Matrix and vector organization

Build distinct matrix and vector units. The matrix unit must support
matrix–matrix multiplication, matrix–vector multiplication, and vector outer
products. The vector unit implements element-wise operations, reductions,
conversions, and the primitives used to construct activation and normalization
kernels. Start implementation with the matrix processing element and vector
lane arithmetic. The planned primitives include add/subtract/multiply,
saturating arithmetic, shifts, sum/argmax/max/absolute-max reductions, type
conversions, exponent, and square root/reciprocal square root. Addition and
reductions are the first vector priorities across the supported data types.
See October 3 at 40:01, 44:56, 51:24, 54:14, and 116:01.

Array dimensions and vector lane count remain parameters. The October 10
discussion favors sweeping lane counts against actual workload lengths and area
cost; the presented eight-lane design processing 32 elements over four cycles is
an implementation candidate, not the selected size. Keep the two current vector
designs separate for comparison before reconciling them into one design
(October 10, 36:20–42:05 and 58:24).

### Programmable vector operations and command control

Implement activation and normalization kernels as programmable sequences of
SIMD primitives. Firmware supplies sequences such as softmax, sigmoid, SiLU,
and ReLU. The SIMD array has no control flow of its own; a local controller
sequences its operations. This lets the team add kernels without building a
separate fixed-function datapath for each activation (October 3, 44:56–51:24).

The device-side RISC-V core submits commands to the top-level command sequencer,
which distributes unit-specific commands to the matrix and vector units. The
vector unit also needs a secondary core or sub-command sequencer to issue the
steps within an operation. The matrix unit does not need that vector-specific
path (October 10, 16:38). Selecting the vector controller implementation remains
open; the options discussed are a small RISC-V core and a runtime-configured
lookup-table sequencer.

Keep the RISC-V core basic and control the SIMD array through MMIO or reserved
registers; the exact access mechanism remains open. Custom SIMD commands do not
imply a custom CPU or an extension to the CPU's RISC-V ISA. The host/firmware
decomposition split remains tracked by [architecture #7][issue7].

### SIMD command width and ownership

Use fixed-length **32-bit SIMD commands**. October 10 at 22:19 confirms the
width, resolving the earlier mismatch. Compute owns the SIMD instruction-set
definition (October 3, 54:14). The [ISA documentation task][isa-task] calls for
publishing the bit layout, field meanings, and instruction behavior in GitHub
and reconciling the older 40-bit description.

This width decision applies to SIMD commands. It does not set the top-level
command or descriptor layout, whose software-visible contract is tracked by
[architecture #3][issue3]. Register count, opcode encodings, and complete
instruction semantics still need a shared specification.

### SRAM exchange and dependency tracking

Move data between compute units through SRAM, with **no forwarding in the first
version**. The scoreboard tracks dependencies, including compute and writeback
status, so the SRAM arbiter does not duplicate RAW/WAR hazard checks. This
separates dependency scheduling from memory-request arbitration (October 3,
66:58; also the [SRAM arbiter documentation task][arbiter-task]).

For the next SRAM interface proposal, replace the lane-mask input with a one-bit
transpose control (October 10 follow-up task). The proposed transpose read uses
staggered addresses across banks. Transfer width, bank count, handshake details,
and any extra vector-control signals remain open; the presented 512-byte
transfer is not a frozen width (October 10, 24:13–28:49 and 58:24).

### Numerical direction

The team selected an integer weight/activation direction with higher precision
where the model needs it. The October 3 discussion at 36:54–44:56 establishes
the following implementation plan; the [October 10 block-scaling task][scaling-task]
continues from the INT4/INT8 weight and INT8 activation plan.

| Data or operation | Selected direction | Details still to resolve |
|---|---|---|
| Weights | Signed INT4 or INT8, with block and per-tensor scales | October 3 describes one scale per 16 elements; the block-scaling task still requires agreement on block size, scale encoding, delivery, and placement in the datapath. |
| Activations and ordinary matrix results | INT8 activations, INT32 accumulation, then requantization to INT8 | Rounding, saturation, overflow, and application of scales. |
| Q/K values | INT16 blocks sharing an exponent | Keeping these values entirely within the vector unit was an expectation Zeb still needed to check. Storage and cross-unit handling remain open. |
| Gated DeltaNet decay math | Q8.24 fixed point to preserve small decay terms | Partial-product implementation, intermediate precision, and the complete recurrent-state contract. |
| Vector lane arithmetic | INT16/INT32 and FP16/FP32; dequantize, compute in floating point where needed, then requantize once | Conversion semantics and sharing of integer/floating-point hardware. |

All-integer activation experiments were reported to cause large accuracy drops,
which motivated the floating-point vector path. The notes do not supply a
reproducible model-quality result or a complete numerical contract. Keep
[architecture #9][issue9] open for tensor/state formats, arithmetic rules, and
quality evidence before freezing numerical interfaces. Floating-point exponent
support is planned, but its implementation still needs design discussion
(October 3, 116:01; October 10, 49:03).

### Implementation and review

Target FPGA implementation before tape-out (October 10, 13:04). Whether FPGA
and ASIC targets need separate RTL remains unresolved.

Publish work on branches in the club RTL repository and merge through pull
requests. Put matrix RTL and its corresponding testbench in their respective
compute folders under the RTL and testbench directories. Share the current
matrix implementation before waiting for the stationary-output change and SRAM
wrapper (October 10, 9:15 and 18:14). Use SystemVerilog with descriptive names,
two-space indentation, explicit ports, and named connections. Authors must read
and understand AI-generated RTL before submitting it (October 3, 84:07).

## Alternatives and evidence

| Choice discussed | Decision or remaining comparison | Evidence and limits |
|---|---|---|
| Hardwired activation units versus programmable SIMD sequences | Select programmable sequences. | October 3, 44:56–51:24: flexibility for new activations and variable-length operations. No measured controller cost was established in the meeting. |
| Forwarding versus exchange through SRAM | Start with SRAM and no forwarding. | October 3, 66:58: simpler initial integration. September 28's limited interconnect experiment estimated about 1–2% improvement for its configuration; that is not a general bandwidth result. |
| All-integer versus mixed integer/floating-point vector math | Retain floating-point support for operations that need it. | October 3, 44:56: reported accuracy loss with all-integer activation math; full numerical validation remains open. |
| Stationary A versus stationary C in the matrix array | Stationary C is the favored next change, not completed RTL or a frozen dataflow decision. | October 10, 3:35–9:15: keep wider accumulated sums in place. Tiling and removing shadow registers are area proposals; presented area figures lacked synthesis constraints. |
| Small RISC-V core versus configured lookup-table vector sequencer | Controller implementation remains open. | October 3, 44:56; October 10, 16:38: either must sequence the SIMD primitives locally. |

## Remaining integration decisions

Compute and Controller still need to agree on memory-request wrappers, interface
signals, and scoreboard communication. Ownership of the vector memory-request
wrapper is explicitly deferred to the next meeting (October 10, 55:47). Matrix
INT4 support and block scaling remain implementation work, not demonstrated
features of the presented matrix unit.

The complete primitive specification, physical lane and register counts,
matrix buffering/accumulator organization, and SRAM bank/transfer sizing remain
open. In particular, packed INT4 multiplication, chained accumulators, and
serial Q8.24 partial products were discussed as proposals, not final arithmetic
implementations. Command acceptance/completion, errors, reset, and persistent
state ownership still require the shared
[boundary contracts](../contracts/accelerator-boundaries.md).

## Revisit conditions

Revisit numerical choices if matched kernel or full-model quality checks expose
unacceptable error, especially across long decode and recurrent-state updates.
Revisit SRAM-only exchange if measured contention or bandwidth limits justify
forwarding. Select lane counts, matrix dataflow, and local control using workload
utilization and constrained implementation results. FPGA and ASIC resource
constraints can require different implementations; the meeting's unconstrained
area estimates do not settle those choices.

[oct3]: https://app.notion.com/p/3ee38826be1b81668497e19a4ea5994f
[oct10]: https://app.notion.com/p/3f538826be1b81e1a8e0d468ad655828
[sep28]: https://app.notion.com/p/3e938826be1b810889c4f4a0b672ccad
[isa-task]: https://app.notion.com/p/3f538826be1b8179a1fbdaa6102ba1d0
[scaling-task]: https://app.notion.com/p/3f538826be1b80118724cf866a8db148
[arbiter-task]: https://app.notion.com/p/3f538826be1b807dbbf3ed85a86565e6
[issue3]: https://github.com/SiliconBadgers/architecture/issues/3
[issue7]: https://github.com/SiliconBadgers/architecture/issues/7
[issue9]: https://github.com/SiliconBadgers/architecture/issues/9
