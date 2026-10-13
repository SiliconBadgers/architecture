# Cross-team open decisions and exploration ranges

Status: **register for review**, last checked **2026-10-13 UTC**. This inventory
responds to [Akanksha's request on architecture #13][request]: keep settled
choices in the baseline, enumerate the questions teams are exploring, and
publish ranges Software can model. Adding a row here does **not** approve a
parameter, assign a person, change an interface, or close the linked work.

## How to read this register

- **Open** means the cited source explicitly leaves a decision or contract open.
- **Proposal** means a concrete option exists but is not accepted. Review comments
  are requirements to resolve, not proof that their suggested implementation won.
- **Evidence gap** means a source identifies missing validation, calibration or
  specification. This is not a claim that a new hardware feature is required.
- **Explored** ranges are reproducible study inputs, not team-approved design
  bounds. A baseline value, example, sensitivity interval or hardware maximum is
  not an agreed sweep range. **Agreed bounds: TBD** unless stated otherwise.
- Each row has a stable ID, one related decision family, current constraints or
  options, evidence needed, and sources. Subquestions in a family must all be
  resolved before closing it. Split a family into child IDs when useful.
- Team headings identify participants, not newly assigned owners. **Decision authority:
  TBD for every row** until the affected teams confirm one. Existing named contributors are recorded below where explicit; this does not
  reassign their work or make them the sole decision authority.
- Every row was checked on the date above. Later updates should record a row's
  own verification date and changed source revision. `N/A` means a behavioral or
  scope choice rather than a numeric sweep; it does not mean resolved.

## Baseline to preserve

The merged [compute decisions][compute] record matrix–matrix, matrix–vector and
outer-product support; stationary-output support with write/retain control;
vector elementwise, reduction, conversion and activation/normalization work;
firmware-defined kernels; **fixed 32-bit SIMD commands**; and **local RISC-V issue
of SIMD primitives with no control flow in the SIMD array**. The detailed
[SIMD ISA][isa] and [signature catalogue][signatures] are separate from the
system job/descriptor ABI. Do not reopen instruction width because an older
meeting had a mismatch.

The numerical direction is initial, pending [architecture #9][a9]: INT4/INT8
weights with block/per-tensor scales; INT8 activations; ordinary matrix INT32
accumulation then INT8 requantization; Q/K INT16 blocks sharing an exponent;
Q8.24 DeltaNet decay; vector floating-point work/conversions where needed.
This is neither a proof of model quality nor permission to replace those choices
with the older slide's BF16/FP32 example. Q/K placement remains explicitly open.

The initial exchange path is shared SRAM, without a separate compute-to-compute
fabric. The four boxes in the [central diagram][diagram] describe functions,
not four mandatory physical engines. One command in flight and the 128-byte
system descriptor remain [slide comparison baselines][maps], not a frozen ABI.

## Open-decision register

### Compute: matrix and vector, with Software and Memory

| ID / status | Question and current constraint/options | Ranges / bounds | Evidence needed and dependent work | Sources |
|---|---|---|---|---|
| C01 · Open | What matrix array dimensions, array count, tile shapes and fill/drain schedule suit prefill and decode? Stationary-output support is fixed; PE grouping, buffering and scheduling details are not. | Agreed bounds TBD; E02/E03 are explored settings. | Shape/tail utilization, SRAM feed, constrained synthesis and measured clock. Feeds M01, M02 and P02. | [Compute][compute], [boundaries][boundaries], [engine assumptions][engine], [Compute Oct 10, 3:35/9:15][mt-compute] |
| C02 · Open | What are the exact block/per-tensor scale representation, block size, scale application, packing and requantization rules? What type is used by outer products? | INT4/INT8 weight direction; exact scale/outer-product choices and bounds TBD. The old group=64 example is not approval. | Common numerical/reference vectors and model quality; reconcile with N01 and memory layout M03. | [Compute][compute], [maps][maps], [Software Oct 11, 1:45][mt-software] |
| C03 · Open | How are matrix commands, accumulator clear/retain/write behavior, input buffering and SRAM wrapper integrated with the scoreboard? | Fixed stationary-output capability; command fields and interface bounds TBD. | Accepted-command traces, backpressure, accumulator lifetime and output ownership; blocks controller/Compute integration. | [Compute][compute], [Compute Oct 10, 3:35/18:14][mt-compute], [architecture #3][a3] |
| C04 · Open | What physical vector lane/engine count, register-file implementation and resource allocation should the reconciled implementation use while complying with the published ISA? | Preserve ISA V0–V7/S0–S7/P0–P7, 64-bit cells, VL and masks. Physical sizing bounds TBD; the eight-lane/32-element design is historical, not an ISA change. E01 records past exploration. | Compare actual vector lengths, area, decoder/unsigned arithmetic compatibility and the published ISA; reconcile the two implementations. | [Compute Oct 10, 36:20/42:05][mt-compute], [ISA][isa], [engine][engine] |
| C05 · Open | Who implements the vector memory-request wrapper, and which commands, requests, return-data writes and additional arbiter signals does it own? | N/A for ownership; signal widths/queue bounds TBD. | Agree command format and M03–M06 before wrapper integration; record an explicit owner. | [Compute Oct 10, 55:47/58:24][mt-compute] |
| C06 · Open | What implementation, throughput, latency and accuracy do exp, reciprocal/rsqrt, reductions and conversions provide? How are firmware kernels mapped onto the primitives? | Primitive/signature scope is recorded; implementation bounds TBD. E01 has exploratory throughput/latency points only. | Implementation compliance with published numerical/fault semantics, constrained synthesis, pipeline hazards and representative softmax/RMSNorm/SiLU tests. | [Compute][compute], [ISA][isa], [vector study][vector-study], [Compute Oct 10, 49:03][mt-compute] |
| C07 · Open | Is shared matrix/vector arithmetic sufficient for attention, convolution and recurrence, or does dedicated arithmetic justify its cost? What serial/chunked/matrix recurrence lowering is actually supported? | Matrix/vector direction fixed; dedicated engines and lowering choices remain open. E02/E03 are modeling alternatives. | End-to-end dependencies, five-read/two-write state traffic in current engine, useful occupancy, software lowering and synthesis. Do not interpret a simulator `recurrent` resource as a hardware decision. | [boundaries][boundaries], [engine][engine], [system][system] |

### Numerical and workload contract: Software, Compute, Verification, Architecture

| ID / status | Question and current constraint/options | Ranges / bounds | Evidence needed and dependent work | Sources |
|---|---|---|---|---|
| N01 · Open / evidence gap | What versioned model-wide numerical contract and interface-freeze decision validate the initial recipe, including accumulation, rounding/saturation, overflow, scales and conversion? | Initial formats above narrow exploration; supported alternatives, model tolerances and remaining contract TBD. Published SIMD primitive semantics stay fixed unless explicitly revised. | Kernel/reference comparisons and end-to-end task-quality checks. Q4_K_M profiling alone does not validate the custom INT4 recipe. | [architecture #9][a9], [compute][compute], [engine][engine] |
| N02 · Open | Do INT16 shared-exponent Q/K values stay entirely within the vector unit? What cross-unit representation and conversion boundaries follow? | Agreed bounds TBD; Q/K direction is initial, placement is explicitly unresolved. | Attention dataflow, SRAM layout and command interface compatibility; affects C06/C07, M03 and N01. | [compute][compute] |
| N03 · Open | What precision, representation and lifetime apply to KV cache, recurrent state and convolution history beyond the explicitly recorded Q/K and decay choices? | Agreed bounds TBD; engine `act_bits=16`, `kv_bits=16`, `state_bits=32` are assumptions, not the newer team's INT8-activation decision. | Long-context/multi-token error and storage cost, reference state transitions, reset/replay behavior. | [system][system], [architecture #9][a9], [engine][engine] |
| N04 · Open | Which common model/quantization/graph baseline should new sweeps use, and how is the discussed custom quantized recipe exported to reproducible GGUF/graph inputs? | Qwen3.5-2B and mixed Q4_K_M are recorded workload evidence; new recipe and acceptance criterion TBD. | Pin model/hash, converter/version, prompt/microbatch/context and capture exclusions; keep optimizations separate from baseline. | [workload cases][workloads], [Software Oct 11, 38:14/57:50][mt-software] |

### Memory and transfers: Memory, Compute, Control, SoC

| ID / status | Question and current constraint/options | Ranges / bounds | Evidence needed and dependent work | Sources |
|---|---|---|---|---|
| M01 · Open | What SRAM capacity, bank count, ports, physical row width and per-cycle service are realizable on the target? | Agreed bounds TBD. PR #18's 8 MiB/32 banks/512-byte row and engine's 8 MiB/64 banks are different proposals/assumptions, not a common baseline. E01/E02/E03 are explored ranges. | Macro/BRAM/URAM mapping, clocked access tests, conflicts and Compute feed demand; affects C01/C04, P02. | [RTL #18][r18], [engine][engine], [Compute Oct 10, 28:49][mt-compute], [Software Oct 11, 43:39][mt-software] |
| M02 · Open | How are activations, weights/scales, partial sums and persistent state placed, reserved, tiled, spilled and prefetched? Can double buffering actually overlap? | Agreed bounds TBD; current engine partition/residency/fusion choices are assumptions (E02). | Liveness and working sets, output-head traffic, port-constrained overlap and target capacity. Required for realistic performance sweeps. | [system][system], [diagram][diagram], [workloads][workloads], [engine][engine] |
| M03 · Open | What tensor layout, address/stride units, alignment, transpose/bank mapping and data-type-dependent access rules do Compute and SRAM share? | Byte strides in slide baseline; final layout/alignment restrictions TBD. Diagonal banking is a proposal. | Row/column/tail accesses for supported widths, transpose tests and bank conflicts; feeds C02/C05 and M04. | [boundary worksheet][boundaries], [Controller Oct 6, 17:51][mt-control], [RTL #18][r18] |
| M04 · Proposal | Is a 4096-bit row write mask byte-granular (512 enables) or 64 enables for 8-byte chunks? Which sizes/alignments are supported? | Competing interpretations, not a numeric sweep; agreement TBD. | Reconcile Step 4 and signal definitions in #18; partial-write/tail reference tests. | [RTL #18 review][mask-review] |
| M05 · Proposal | Does the memory manager submit separately handshaken single beats, or does the SRAM arbiter own a multibeat burst? Where do length, address progression, write data and completion live? | Proposed 512-byte beats; allowable burst range TBD. A 10-bit byte count does not encode the advertised multibeat contract. | Revised metadata/handshake trace and per-beat versus per-burst completion; blocks transfer/controller integration. | [RTL #18 review][burst-review] |
| M06 · Proposal | How many requests may be outstanding per source, how are repeated source tags matched to responses, and do writes produce response-valid? How does the scoreboard gate dependent requests and safe reuse? | Tags 0–5 identify sources in #18; outstanding limits/ordering agreement TBD. | Define scoreboard ownership, request identity, backpressure, arbitration/fairness and release point; delayed/reordered-response tests. | [RTL #18 review][order-review], [Controller Oct 6, 20:24][mt-control], [boundaries][boundaries] |
| M07 · Open | What HBM-to-SRAM command, queue/outstanding model, prefetch policy and integration with the arbiter are needed? What is DMA's architectural role and verification boundary? | Agreed bounds TBD; `dma.count=2`, 64 bytes/cycle are engine assumptions. | Command format plus arbiter/SRAM I/O; accepted-request accounting and integration tests. | [Controller Oct 6, 43:12/49:12/58:25][mt-control], [Verification Oct 12, 23:09][mt-verification], [engine][engine] |
| M08 · Evidence gap | What sustained HBM/DDR and SRAM bandwidth, latency and conflict/response behavior should replace model inputs, and how should HBM IP be validated before/after FPGA access? | Agreed bounds TBD; 460 GB/s × 0.7 in the engine is an assumption, not a measurement. | IP access, simulation and hardware read/write tests; record measured target/clock/traffic. The pre-FPGA versus on-FPGA validation approach remains open. | [engine][engine], [Compute Oct 10, 49:03][mt-compute], [Tech Sync Oct 12, 12:36][mt-sync] |
| M09 · Open | Would direct weight streaming or compute forwarding be worth adding to the shared-SRAM path? | Initial path remains shared SRAM. `via_l1`/`direct` are model alternatives; forwarding is a stretch proposal, bounds TBD. | Size added buffering/conversion/FIFOs and compare contention, traffic and area; no separate fabric is approved here. | [system][system], [Controller Oct 6, 10:24][mt-control], [engine][engine] |

### Control and SoC: Control, Software, SoC, Compute, Memory

| ID / status | Question and current constraint/options | Ranges / bounds | Evidence needed and dependent work | Sources |
|---|---|---|---|---|
| T01 · Open | How are graph decomposition, lowering, dependency tracking, batching and fallback split between host and device-side RISC-V firmware? | RISC-V presence/primitive issue fixed; responsibility split and job granularity TBD. | Workload-to-command traces for prefill, decode and stateful work; distinguish system jobs from 32-bit SIMD primitives. | [architecture #7][a7], [system][system], [compute][compute] |
| T02 · Open | What are the final MMIO map and descriptor layout: offsets, widths, byte order, register reset/access/side effects, opcode/flag/format encodings, parameter blocks, capability/status bits, error codes and state IDs? | One in-flight command, 128-byte descriptor/alignment and slide fields are comparison baselines; final bounds TBD. | Source-linked llama.cpp requirements and change rationale; concrete valid/invalid descriptors. Existing named contributors: David Sklow and Adrian Luo (#3); no new assignment. | [architecture #3][a3], [maps][maps] |
| T03 · Open | When is a doorbell accepted, what happens while busy, when are descriptor/buffers immutable, and which validation failures reject without side effects? | Behavioral choice, N/A numeric sweep; acceptance rules TBD. | Malformed/busy submissions, snapshot/lifetime tests and validation ownership. | [architecture #3][a3], [system][system], [boundaries][boundaries] |
| T04 · Open | What device address spaces, platform regions, bounds/alignment, ordering, cache visibility and interrupt rules connect host, firmware, controller and Memory? | Slide region encoding is a proposal; platform address/visibility contract TBD. | Publish/fence/cache-maintenance trace; exact SoC mapping and output visibility point. A CPU fence alone is not the policy. | [architecture #7][a7], [architecture #3][a3], [maps][maps], [SoC #4][s4] |
| T05 · Open | What unit-specific matrix/vector/memory commands, dependency flags, queue depths and scheduling rules does the sequencer use? | SIMD width fixed at 32 bits; system/engine queue dimensions and formats TBD. In-order per-unit queues plus scoreboard are a proposal. | Joint controller/Compute/Memory command contract and dependency/backpressure traces; blocks command issuer and memory-controller RTL integration. | [Controller Oct 6, 20:24][mt-control], [Tech Sync Oct 12, 12:36][mt-sync], [RTL #6][r6] |
| T06 · Open | What does engine start/ready/done/error mean, which resource owns outputs, and when can the next command or consumer proceed? | Latencies/unit counts remain parameters; behavior and numeric bounds TBD. | Variable-latency models, accepted work and delayed writes; align with scoreboard M06 and final ABI. | [boundaries][boundaries], [system][system], [RTL #6][r6] |
| T07 · Open | What constitutes terminal completion, how is sequence identity matched, and how do polling, IRQ, interrupt clearing, acknowledgment and buffer release interact? | Slide ACK/quiescence separation is a proposal; final semantics TBD. | Delay memory responses past arithmetic completion; verify no premature reuse or loss of completion identity. | [architecture #3][a3], [maps][maps], [boundaries][boundaries] |
| T08 · Open | What is persistent request/state ownership and the contract for sequence isolation, token order, initialization, checkpoint/replay and invalidation? | KV/recurrent/history state is required; storage/behavioral policy TBD. | Prefill plus multiple decode steps, interleaved request IDs, reset/reuse and stateful faults; depends on N03/M02. | [system][system], [boundaries][boundaries], [architecture #7][a7] |
| T09 · Open | How do fault, timeout, drain, quiescence and reset propagate, especially after partial state/output writes? | No timeout may silently cancel already accepted traffic; final recovery/reset contract TBD. | Resolve #18 response-discard/reset proposal and #10 error→IRQ bypass versus drain-before-completion; define backpressure versus permanent stall/watchdog behavior. Test outstanding transfers, partial state and safe invalidation. | [system][system], [maps][maps], [RTL #18][r18], [RTL #10][r10] |
| T10 · Open | Which existing RISC-V/core integration, boot/firmware, memory map and host/platform interfaces realize the working design? | No custom CPU/ISA implied; exact integration TBD. | SoC integration proposal, executable firmware/command trace and target-specific interface tests. | [SoC #4][s4], [system][system] |

### Software model and verification evidence

| ID / status | Question and current constraint/options | Ranges / bounds | Evidence needed and dependent work | Sources |
|---|---|---|---|---|
| S01 · Evidence gap | Which joint compute/memory sweeps and target constraints should form the current shared simulator baseline? Which historical assumptions must be retired or recalibrated? | Agreed team bounds TBD; exploration inventory below. | Map each sweep axis to a decision ID, pin configuration/graph, include stalls/dependencies and measured calibration. Start with compute and local memory as agreed discussion scope. | [request][request], [Software Oct 11, 21:20/26:27/62:43][mt-software], [engine][engine] |
| S02 · Open | Which tiling, fusion, residency, causal skipping, KV padding/masking, softmax overlap and schedule assumptions correspond to an implementable lowering? | Current engine switches are alternatives, not decisions; numeric bounds TBD. | Runnable lowering, finite buffers/queues and dependency checks; compare prefill/decode and conservative alternatives without treating estimates as measured throughput. | [engine][engine], [workloads][workloads] |
| S03 · Evidence gap | What measured timing/resource models replace clock, utilization, format-rate, recurrence, DMA, launch/synchronization and host-link placeholders? | Agreed bounds TBD; ±30% model sensitivity is uncertainty analysis, not an approved hardware range. | Exact RTL/target/configuration and representative traffic; trace costs to C01/C06/C07/M08/T05/P02. | [engine][engine], [Software Oct 11, 14:32/30:06][mt-software] |
| V01 · Open | What are the verification subsystem boundaries, supplied-IP versus own-IP responsibilities, and required interface/requirement-to-test mapping? | N/A numeric sweep; agreement TBD. | Design/interface diagrams, DMA boundary M07, test-plan coverage linking acceptance, state, backpressure and faults; do not equate onboarding examples with full-design verification. | [Verification Oct 12, 16:09/23:09/27:41][mt-verification], [Tech Sync Oct 12, 8:07][mt-sync] |
| V02 · Open | What shared RTL/UVM build structure, file lists, supported simulator configurations and integration checks should teams use? | Synopsys flow required by verification #2–4; shared build/reuse/integration choices TBD (N/A numeric sweep). | Reproducible unit/system runs with documented tool-specific differences; consolidate rather than assuming independent examples prove integration. | [Tech Sync Oct 12, 8:07][mt-sync], [Controller Oct 6, 53:15][mt-control], [verification #4][v4] |
| V03 · Open / evidence gap | What per-layer methodology, independent reference/scoreboard, exact-versus-tolerance comparison, coverage and completion criteria establish confidence in the design? | Synopsys tools required. UVM, simpler SV and C/C++ roles/DPI integration must be justified per layer; numerical tolerances and coverage goals TBD, not invented percentages. | Versioned requirements-to-test/coverage mapping, independent models, demonstrated RTL integration and passing/failing/timeout pilots. A C++ model, example or stub pass is not full-design verification. | [verification #2][v2], [verification #3][v3], [verification #4][v4] |

### Platform and Physical Design, with Architecture and SoC

| ID / status | Question and current constraint/options | Ranges / bounds | Evidence needed and dependent work | Sources |
|---|---|---|---|---|
| P01 · Open | What exact target envelope and success metric bound exploration, and what subset of the FPGA design could become a useful tapeout? Is separate RTL required? | FPGA-first direction; full-versus-subset tapeout unresolved. Resource/performance bounds TBD. | Agree practical FPGA capacity and objective, representative-block value, external memory/I/O and test plan. October 12 simulation-token semester goal supersedes the earlier October 6 semester-FPGA goal; early-next-semester FPGA is proposed. | [system][system], [Software Oct 11, 46:10][mt-software], [Compute Oct 10, 13:04][mt-compute], [Tech Sync Oct 12, 20:33][mt-sync] |
| P02 · Evidence gap | What clocks, memory macros, utilization, I/O timing and area/resource limits can the actual FPGA/ASIC flow support? What constraints/corners make comparisons meaningful? | Agreed bounds TBD. Engine cost/DSP proxies are not area, power, price or proof of fit. | Reproducible tool/library/RTL/SDC manifest; real-unit and stub results clearly separated; constrained timing, memory mapping and fit reports. | [engine][engine], [physical-design #2][p2], [physical-design #3][p3], [PD Oct 6, 23:10/64:22][mt-pd] |
| P03 · Open | Which manufacturing path, process/PDK access, memory/IP availability, package/pins, board/test and clocking arrangement is feasible for an eventual chip? | Agreed bounds TBD; process/shuttle discussions are investigations, not commitments. | Verified access/constraints and testable implementation scope; keep FPGA and ASIC assumptions separate. | [system][system], [Physical Design overview][pd-overview], [Compute Oct 10, 13:04][mt-compute] |

Current Physical Design issues #2/#3 are baseline flow/report tasks, not authority
for a new parameter-sweep campaign. Record constraints and limitations first;
this register does not expand their scope.

## Existing exploration ranges: usable evidence, not approved bounds

These are exact recorded study inputs or explicitly labeled model choices. All
**team-approved future sweep bounds remain TBD**. Use the pinned originals for
coupled axes, fixed parameters, units, workload and limitations; do not construct
an arbitrary Cartesian product from this summary. Preserve dated experiments.

### E01: architecture vector-control study (October 2)

Pinned at architecture `2ea76238ed55e7d562ec28bbbd3d289eb5546d97`,
[`run.cjs`][vector-run] and [study limitations][vector-study]. Relevant to C04,
C06, M01, M02 and T05. These historical comparisons include control alternatives
that predate the recorded RISC-V direction; their existence does not reopen it.

| Study | Axis | Recorded points and units |
|---|---|---|
| Cartesian | Kernel/row length | Softmax, RMSNorm, SwiGLU; 128, 2,048, 6,144, 8,192, 20,736 elements |
| Cartesian | Engines; lanes/engine | 1, 4, 8 engines; 16, 32, 64 lanes |
| Cartesian | Shared SRAM; scratch capacity | 16, 64, 256 bytes/cycle aggregate; 0, 16, 64, 512 KiB/engine |
| Cartesian | Special-function throughput; RISC-V issue cost | 1, 4, 16 elements/cycle/engine; 1, 4, 12 cycles |
| Cartesian | Controllers; dispatch overlap | 1 or engine count; false/true |
| One-variable sensitivities | Engines; lanes | 1, 2, 4, 8, 16; 8, 16, 32, 64, 128 |
| One-variable sensitivities | Shared SRAM; scratch bandwidth | Each 16, 32, 64, 128, 256, 512 bytes/cycle (scratch is per engine) |
| One-variable sensitivities | Scratch capacity | 0, 16, 64, 128, 256, 512 KiB/engine |
| One-variable sensitivities | Special-function throughput; latency | 1, 2, 4, 8, 16, 32 elements/cycle/engine; 4, 12, 32 cycles |
| One-variable sensitivities | Reduction cadence; RISC-V issue cost | 1, 2, 4, 8 cycles; 1, 2, 4, 8, 12, 24 cycles |
| One-variable sensitivities | Controllers; engines/command; controller/datapath clock ratio | 1, 2, 4, 8; 1, 2, 4, 8; 0.25, 0.5, 1, 2 |

The study does not simulate bank conflicts, finite queues, instruction-fetch
stalls, actual FPGA routing/area/power or timing closure. Its effective bandwidth
and FP32 temporaries are assumptions, not the final hardware/numerical contract.

### E02: maintained Software engine assumptions

Pinned Software revision `0e06023d74c06cc12bb9e05d9e65102347ecc3f0`:
[assumption register][engine] and [sweep implementation][engine-sweep]. These
are baseline placeholders or categorical comparisons, **not agreed ranges**.
The engine explicitly says none are Compute-, Memory- or Control-team decisions.

- Physical/design axes needing team bounds: clock; matrix count/rows/columns,
  tile K and format rates; vector count/lanes and special-function cycles;
  recurrence count/lanes/scratch/chunk and matrix penalty; DMA count/width;
  SRAM capacity/banks/width/efficiency/partition; HBM capacity/useful bandwidth;
  launch/synchronization, fallback core and host-link costs.
- Modeling alternatives: `via_l1`/`direct` weight paths; captured/uniform INT4/
  uniform INT8 weights; fusion `none`/`chains`/`groups`; residency `belady`/
  `per_op`; serial/pool scheduling and overlap; causal skip, on-chip mask,
  captured/exact KV padding; serial/chunked/matrix/auto recurrence lowering.
- Default sensitivity perturbs selected parameters by ±30%; integer fields are
  rounded and efficiency is capped at 1. This is a model uncertainty experiment,
  not a hardware min/max specification.
- The current recurrence model uses five state reads and two writes per token.
  Older frozen JavaScript studies must retain their original assumptions and
  cannot be compared as if they had this correction automatically applied.
- Example disagreements requiring explicit mapping: current engine defaults have
  16-bit activation storage and 64 SRAM banks, while the initial compute record
  says INT8 activations and SRAM PR #18 proposes 32 banks. Neither simulator
  defaults nor an unmerged proposal may silently override the shared baseline.

### E03: other historical Software sweeps

Pinned at the same Software revision as E02. The [compute-mapping index][mapping]
links each report; exact inputs are in the [September 28][sw-sweep-1],
[September 30][sw-sweep-2], [October 1][sw-sweep-3] and [October 3][sw-sweep-4]
specifications. These are older JavaScript-model experiments, not reruns of the
current Python engine or numerical validation of the latest compute recipe.

| Historical study | Exact exploratory axes | Fixed context / limitations |
|---|---|---|
| Sep 28 resource sensitivity and Sep 30 dependency/resource sensitivity | Matrix and vector count each 1, 2, 4, 8, 16, 32; dedicated recurrence count 0, 1, 2, 4, 8, 16; DMA count 1, 2, 4, 8, 16; SRAM banks 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024; peak HBM 25, 50, 100, 200, 400, 800, 1600 GB/s; SRAM capacity 0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16, 32 MiB | One-dimensional sweeps, batch 1, prompt 512, context 2048, `w8a16`; plateau threshold 0.02. Large points are explorations, not supported hardware. |
| Oct 1 joint matrix/SRAM/HBM | Matrix count 1, 2, 4, 8, 16; SRAM banks 16, 32, 64, 128, 256; HBM 100, 200, 300, 400, 460 GB/s | Batch 1, prompt 512, context 2048, `w8a16`; vector/recurrent/DMA counts 4/4/1, SRAM 8 MiB. Study caps HBM at 460 and uses configured DSP budget after shell reserve; these do not prove target fit. |
| Oct 3 recurrence mapping sensitivity | Matrix and dedicated recurrence counts each 1, 2, 4, 8, 16; matrix penalty 1, 2, 4, 8, 16, 32; `w8a16` and `w4a8`; coupled memory profiles (32 banks, 100 GB/s), (128, 300), (256, 460) | Captured pp128/pp512 prefill/decode; target prompt/context 512/2048 at batch 1 or 8; vector 4 × 32 lanes, DMA 1, SRAM 8 MiB. Preserve original recurrence equation; current engine correction is not retroactive. |

Relevant to C01/C04/C07, M01/M02/M08, N04 and S01–S03. Re-evaluate which axes
remain meaningful under the recorded compute decisions before generating new
plots; do not copy the old `w8a16` or recurrence-resource choices into a frozen
hardware baseline.

## Closing and maintaining a decision

1. Teams add missing source-backed questions or split existing IDs; supply an
   explicit owner only with that person's/team's agreement. A new inferred gap
   must be marked **inferred**, with why it matters, rather than presented as an
   established team decision.
2. For each numeric exploration, publish parameter key, units, discrete points or
   min/max/step, fixed constraints, coupled exclusions, target, workload, metric
   and source revision. Leave **TBD** where not agreed; distinguish a suggestion
   from an approved range. For a behavioral choice, list alternatives and traces.
3. Attach evidence/results to the same ID, including limitations and numerical
   correctness. A plot, passing example or merged scaffold alone does not resolve
   a shared contract. Keep the raw configuration and reproducible command.
4. Once affected teams agree, write/link a [decision record][template], date and
   owner; mark the row resolved with a selected value/behavior and revisit
   condition. Update simulator configuration and the shared diagram/contracts
   together. Archive superseded exploration rather than rewriting its history.
5. Update this register promptly with each accepted decision or new open question,
   and review it in team syncs so Software can prune settled axes from new sweeps.
   This maintenance proposal creates no new deadline or assignment.

## Coverage and limits

This is intended to enumerate **all open decision families found in the reviewed
sources**, not certify that every possible hardware unknown has been discovered.
The snapshot covers the architecture main documents at the SHA above, linked
team work and review discussions, current Software engine assumptions, and
October 6–12 Controller, Compute, Software, Verification, Physical Design and
technical-sync meeting notes. Source links below identify the evidence. Meeting
notes report discussions; tentative ideas remain tentative. Some Notion links
may require team access; the actionable question is reproduced in each row.

Discord coverage is limited to the latest 100 messages returned from the
technical-team channel, spanning October 1–13. The [October 13 documentation
discussion][discord-docs] reinforces a central, linked decision record; no numeric
sweep bounds were found in that sample. Compute, Controller, Software,
Verification, Physical Design and technical-leads channel reads were denied, so
their current chat history is not covered. Team review should add newer chat-only
agreements, the October 13 controller/memory discussion if available, undocumented
range bounds and any unreviewed implementation decisions. The register's empty
owner/bounds fields are deliberate gaps to resolve, not invented defaults.

## Sources

[request]: https://github.com/SiliconBadgers/architecture/pull/13#issuecomment-6157385434
[compute]: compute-team-decisions.md
[template]: decision-template.md
[diagram]: ../docs/accelerator-diagram.md
[system]: ../contracts/system-boundaries-and-evidence.md
[boundaries]: ../contracts/accelerator-boundaries.md
[maps]: ../docs/register-maps.md
[workloads]: ../docs/workload-cases.md
[a3]: https://github.com/SiliconBadgers/architecture/issues/3
[a7]: https://github.com/SiliconBadgers/architecture/issues/7
[a9]: https://github.com/SiliconBadgers/architecture/issues/9
[r6]: https://github.com/SiliconBadgers/rtl/issues/6
[r18]: https://github.com/SiliconBadgers/rtl/pull/18
[s4]: https://github.com/SiliconBadgers/soc/issues/4
[p2]: https://github.com/SiliconBadgers/physical-design/issues/2
[p3]: https://github.com/SiliconBadgers/physical-design/issues/3
[isa]: https://github.com/SiliconBadgers/rtl/blob/c1e9dcf7f205994270204132cd87c62781176333/docs/simd-isa.md
[signatures]: https://github.com/SiliconBadgers/rtl/blob/c1e9dcf7f205994270204132cd87c62781176333/docs/simd-isa-signatures.md
[mask-review]: https://github.com/SiliconBadgers/rtl/pull/18#discussion_r4251803644
[burst-review]: https://github.com/SiliconBadgers/rtl/pull/18#discussion_r4251803651
[order-review]: https://github.com/SiliconBadgers/rtl/pull/18#discussion_r4251803661
[vector-study]: https://github.com/SiliconBadgers/architecture/blob/2ea76238ed55e7d562ec28bbbd3d289eb5546d97/research/2026-10-02-vector-control/README.md
[vector-run]: https://github.com/SiliconBadgers/architecture/blob/2ea76238ed55e7d562ec28bbbd3d289eb5546d97/research/2026-10-02-vector-control/run.cjs
[engine]: https://github.com/SiliconBadgers/software/blob/0e06023d74c06cc12bb9e05d9e65102347ecc3f0/engine/docs/ASSUMPTIONS.md
[engine-sweep]: https://github.com/SiliconBadgers/software/blob/0e06023d74c06cc12bb9e05d9e65102347ecc3f0/engine/sbengine/sweep.py
[mapping]: https://github.com/SiliconBadgers/software/tree/0e06023d74c06cc12bb9e05d9e65102347ecc3f0/research/compute-mapping
[mt-software]: https://app.notion.com/p/3f638826be1b816d957ee6404acd16cf
[mt-compute]: https://app.notion.com/p/3f538826be1b81e1a8e0d468ad655828
[mt-control]: https://app.notion.com/p/3f238826be1b81ff9d04d4f927a5a3fd
[mt-verification]: https://app.notion.com/p/3f838826be1b815f84daede3314f6389
[mt-sync]: https://app.notion.com/p/3f838826be1b813b8654e35c9dce4bd7
[mt-pd]: https://app.notion.com/p/3f238826be1b8118970bfcbfebf82052
[pd-overview]: https://app.notion.com/p/142f2d95a32541baa84e66958b08842b

[discord-docs]: https://discord.com/channels/1547296573023719548/1547802617755992125/1559696795398045767
[sw-sweep-1]: https://github.com/SiliconBadgers/software/blob/0e06023d74c06cc12bb9e05d9e65102347ecc3f0/research/compute-mapping/2026-09-28-resource-sensitivity/sweep-spec.json
[sw-sweep-2]: https://github.com/SiliconBadgers/software/blob/0e06023d74c06cc12bb9e05d9e65102347ecc3f0/research/compute-mapping/2026-09-30-dependency-resource-sensitivity/sweep-spec.json
[sw-sweep-3]: https://github.com/SiliconBadgers/software/blob/0e06023d74c06cc12bb9e05d9e65102347ecc3f0/research/compute-mapping/2026-10-01-joint-resource-tradeoffs/sweep-spec.json
[sw-sweep-4]: https://github.com/SiliconBadgers/software/blob/0e06023d74c06cc12bb9e05d9e65102347ecc3f0/research/compute-mapping/2026-10-03-recurrence-multiplier-sensitivity/sweep-spec.json

[r10]: https://github.com/SiliconBadgers/rtl/pull/10
[v2]: https://github.com/SiliconBadgers/verification/issues/2
[v3]: https://github.com/SiliconBadgers/verification/issues/3
[v4]: https://github.com/SiliconBadgers/verification/issues/4
