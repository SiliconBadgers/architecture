# Architecture and shared interfaces

Keep the shared accelerator diagram, interface proposals and evidence-backed decisions in one place. Top-Level Control works here on the software-visible contract and in rtl on the controller itself.

## Start here

1. Read [the current assignment and artifact locations](docs/START-HERE.md).
2. Work on a branch and open a PR for `@abhinavnandwani` using
   [CONTRIBUTING.md](CONTRIBUTING.md). Main requires a code-owner approval;
   admins can bypass.

## Current issues

- [MMIO and command descriptor proposal](https://github.com/SiliconBadgers/architecture/issues/3)

## Repository structure

| Location | Purpose |
|---|---|
| [research/](research/README.md) | Architecture comparisons with reproducible experiments, source evidence, and explicit limitations. |
| [contracts/system-boundaries-and-evidence.md](contracts/system-boundaries-and-evidence.md) | Shared software-to-hardware path, evidence limits and open system contracts. |
| [contracts/register-interface/](contracts/register-interface/README.md) | Proposed MMIO/descriptor tables, baseline comparison, source evidence and command examples for architecture#3. Keep the slide baseline unchanged; a proposal is not an accepted ABI. |
| [decisions/](decisions/README.md) | Accepted decisions and proposals using decision-template.md, with alternatives, supporting evidence and revisit conditions. |

## Open decisions

See the [cross-team open-decision register](decisions/open-decisions.md) for
source-backed unresolved questions, existing exploratory sweep ranges, dependencies,
and explicit TBDs. It preserves the current compute direction and does not approve
new hardware parameters.

## Current material and scope

The [whole-chip diagram](docs/accelerator-diagram.md) records the matrix/vector/memory direction through October 18, with separate compute detail and current RTL/simulation hierarchy. Editable sources, SVGs, PNGs and source revisions are included. The slide maps are preserved in docs/register-maps.md. [Compute team decisions](decisions/compute-team-decisions.md) record the initial numerical and control direction. The final accelerator ABI and detailed compute interfaces remain open.

[Shared diagram](https://github.com/SiliconBadgers/architecture/blob/main/docs/accelerator-diagram.md) · [Software evidence](https://github.com/SiliconBadgers/software/tree/main/experiments/llama-cpp/2026-09-22)

[CHARTER.md](CHARTER.md) and [OBJECTIVES.md](OBJECTIVES.md) describe the
longer-term purpose. Current issues and the starting guide specify the work
assigned now. [SETUP.md](SETUP.md) describes existing example commands and scope.
