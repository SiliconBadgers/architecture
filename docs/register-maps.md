# Proposed MMIO register map and command descriptor

**Status: slide-deck baseline, ABI 0.1, not implemented or finalized.**

These are the two maps from slide 4, “The proposed register and descriptor
contract,” in `SiliconBadgers-Technical-Deck.pptx` from Monday's deck. The table
values below are transcribed directly from the source. One is a register map;
the other is the in-memory command descriptor layout. All offsets are **byte
offsets**. The baseline allows **one command in flight**.

Top-Level Control will refine both maps in **architecture**, using the
[central block diagram](accelerator-diagram.md), llama.cpp source and
[Software's profiling evidence](https://github.com/SiliconBadgers/software/tree/main/experiments/llama-cpp/2026-09-22).
Its detailed controller diagram and command-flow design belong in
[rtl-control](https://github.com/SiliconBadgers/rtl-control/issues/2).
Preserving these tables does not select a custom CPU or ISA, four separate
compute engines, or a final numerical format.

## 1. 32-bit MMIO registers

Register addresses are the platform MMIO base plus the offsets below. The
platform base is not specified by this slide.

| Offset | Register | R/W | Meaning |
| --- | --- | --- | --- |
| 0x00 | ID | RO | 0x53424130 |
| 0x04 | ABI_VERSION | RO | 1 = ABI 0.1 |
| 0x08 | CAPS | RO | Implemented engine bits |
| 0x0C | STATUS | RO | READY / BUSY / DONE / FAULT / QUIESCENT |
| 0x10 | CMD_PTR_LO | RW | Descriptor device address [31:0] |
| 0x14 | CMD_PTR_HI | RW | Descriptor device address [63:32] |
| 0x18 | CMD_BYTES | RW | 128; reset value 128 |
| 0x1C | SUBMIT_SEQ | RW | Matches descriptor SEQUENCE |
| 0x20 | DOORBELL | WO | Write 1: snapshot + submit |
| 0x24 | COMPLETED_SEQ | RO | Last terminal command sequence |
| 0x28 | ERROR_CODE | RO | 0 = success; codes 1-7 |
| 0x2C | IRQ_ENABLE | RW | bit 0 = DONE; bit 1 = FAULT |
| 0x30 | IRQ_STATUS | W1C | W1C: bit 0 = DONE; bit 1 = FAULT |
| 0x34 | ACK | WO | Write 1: release terminal slot |
| 0x38 | CONTROL | WO | bit 0 = QUIESCE; bit 1 = RESET |
| 0x3C | ACTIVE_STATE | RO | Controller state ID 0-10 |

RO = read-only; RW = read/write; WO = write-only; W1C = write one to clear.

## 2. 128-byte command descriptor

The baseline descriptor occupies 128 bytes and requires **128-byte alignment**.
For rows containing multiple fields, the first field occupies the lower address.
Field widths are in bits (`u16`, `u32`, `u64`). The table retains the slide's
field names and grouping.

| Offset | Fields / first field at lower address |
| --- | --- |
| 0x00 | ABI:u16 / OPCODE:u16 / FLAGS:u32 |
| 0x08 | CONTEXT:u32 / SEQUENCE:u32 |
| 0x10 | A device address:u64 |
| 0x18 | B device address:u64 |
| 0x20 | C device address:u64 |
| 0x28 | SCALES device address:u64 |
| 0x30 | STATE device address:u64 |
| 0x38 | PARAMS device address:u64 |
| 0x40 | M:u32 / N:u32 |
| 0x48 | K:u32 / GROUP:u32 |
| 0x50 | A stride:u32 / B stride:u32 |
| 0x58 | C stride:u32 / FORMAT:u32 |
| 0x60 | A allocation bytes:u64 |
| 0x68 | B allocation bytes:u64 |
| 0x70 | C allocation bytes:u64 |
| 0x78 | PARAMS bytes:u32 / RESERVED:u32 |

## Submission, ownership and completion in the source proposal

The slide and its speaker notes describe this sequence:

1. Check `ID`, `ABI_VERSION` and `CAPS` for the interface and supported operations.
2. Wait for `READY`; publish an aligned descriptor and make its contents visible
   to the device. Set `CMD_PTR_LO`, `CMD_PTR_HI`, `CMD_BYTES=128` and `SUBMIT_SEQ`.
   The descriptor's `SEQUENCE` must match `SUBMIT_SEQ`.
3. Write `1` to `DOORBELL` to snapshot the submission registers and submit work.
   The hardware accepts the doorbell only when `READY`.
4. Observe `DONE` or `FAULT`, match `COMPLETED_SEQ` to the submitted command and
   inspect `ERROR_CODE` on failure. Keep the descriptor and buffers frozen until
   terminal completion and ownership release.
5. Write `1` to `ACK` to release the terminal slot only when the hardware is
   quiescent. Clearing the interrupt alone does not release the command slot.

The notes identify descriptor strides as **byte strides** and allocation sizes
as bounds-checking inputs. Ordering and cache visibility need an explicit
policy; the preceding slide notes that a CPU fence alone does not define one.

## Device addresses in the source proposal

A device address encodes `[63:60]` as the memory region and `[59:0]` as a byte
offset. Host pointers are invalid device addresses.

| Source platform | Region 0 | Region 1 | Region 2 |
| --- | --- | --- | --- |
| F2 | HBM | DDR | Descriptor SRAM |
| Caravel | Staging SRAM | Unsupported | Descriptor SRAM |

These are the slide's platform assumptions, retained for review rather than
new platform decisions.

## GEMM example in the source proposal

The slide specifies `opcode=1`, `format=1`, `group=64`, BF16 A/C and scales,
packed symmetric INT4 B, and FP32 accumulation. This is a candidate device
contract, not an automatic match for a GGUF Q4 format. The recorded Software
workload mixes several tensor formats; any conversion and numerical behavior
must be justified.

## What Top-Level Control needs to resolve

Use the real llama.cpp/ggml operation and backend flow to propose the required
registers and descriptor fields, explaining what to retain, change, add or
remove. Define offsets, widths, bit assignments, reset values, access/side
effects, address and stride units, validation and ownership rules. Work through
submission and completion with concrete workload examples and keep unresolved
hardware details explicit so the teams can continue in parallel.

The slide does **not** fully enumerate `STATUS`/`CAPS` bits, error codes 1-7,
controller state IDs 0-10, reset values for every register, descriptor byte
order, all opcode/flag/format encodings, or parameter-block layouts. These are
open design questions, not values to infer from this transcription. The
one-command limit and 128-byte descriptor are also assumptions to evaluate.

## Source provenance

- Deck: `SiliconBadgers-Technical-Deck.pptx`, slide 4 and its speaker notes,
  from the September 21, 2026 presentation material.
- Deck SHA-256: `2c46c9133698c588ff5a4558f544b497a920220877b36e2de7549e1e39912a0b`.
- Slide 4 notes cite *SiliconBadgers Technical Report*, pages 22-23, and
  proposed ABI 0.1 (`proposed/README.md`, `proposed/interface.json`). These are
  source citations, not files claimed to exist in this repository.
- Table transcription added September 22, 2026. No local PowerPoint access is
  needed to read the maps above.
