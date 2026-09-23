# Architecture and shared interfaces: current work

Keep the shared accelerator diagram, interface proposals and evidence-backed decisions in one place. Top-Level Control works here on the software-visible contract and in rtl-control on the controller itself.

## Assignment

- [MMIO and command descriptor proposal](https://github.com/SiliconBadgers/architecture/issues/3)

1. Preserve the two slide register maps as a baseline. Trace llama.cpp/ggml tensor metadata, operations, submission and synchronization at the Software experiment's pinned revision.
2. Propose both the MMIO map and descriptor layout with offsets, fields, access/reset semantics, validation, lifetime and visibility rules. Explain every change against the slide baseline with source or controller evidence.
3. Walk through representative prefill, decode and stateful commands, including completion, errors, reset and safe buffer reuse. Cross-link the controller design in rtl-control.
4. Keep the four compute boxes provisional. Review each Compute team's independent full proposal on its evidence; this scaffold does not choose the final partition.

## Starting evidence

- [Central diagram](https://github.com/SiliconBadgers/architecture/blob/main/docs/accelerator-diagram.md)
- [Recorded Software profiling package](https://github.com/SiliconBadgers/software/tree/main/experiments/llama-cpp/2026-09-22)
- [Slide register maps](https://github.com/SiliconBadgers/architecture/blob/codex/register-map-baseline/docs/register-maps.md) (baseline proposed in [architecture PR #2](https://github.com/SiliconBadgers/architecture/pull/2))

## Artifact locations

| Location | What belongs here |
|---|---|
| [contracts/register-interface/](../contracts/register-interface/README.md) | Proposed MMIO/descriptor tables, baseline comparison, source evidence and command examples for architecture#3. Keep the slide baseline unchanged; a proposal is not an accepted ABI. |
| [decisions/](../decisions/README.md) | Accepted decisions and proposals using decision-template.md, with alternatives, supporting evidence and revisit conditions. |

## What runs today

The central diagram and small MAC example exist. The slide maps are available in PR #2. The final accelerator ABI and compute partition are not decided.

These folders organize the work; they do not complete the issues. Use the
existing evidence now and publish useful intermediate results. Arrange a team
meeting this week to divide the work and agree on next steps.

Follow [CONTRIBUTING.md](../CONTRIBUTING.md) before editing or committing.
