# Architecture and shared interfaces

Keep the shared accelerator diagram, interface proposals and evidence-backed decisions in one place. Top-Level Control works here on the software-visible contract and in rtl-control on the controller itself.

## Start here

1. Read [the current assignment and artifact locations](docs/START-HERE.md).
2. Complete [AI setup and the capture check](docs/git-ai.md) before AI edits or
   your first commit. Every clone needs its local hook activated.
3. Work on a branch and open a PR for `@abhinavnandwani` using
   [CONTRIBUTING.md](CONTRIBUTING.md). Main requires a code-owner approval;
   admins can bypass.

## Current issues

- [MMIO and command descriptor proposal](https://github.com/SiliconBadgers/architecture/issues/3)

## Repository structure

| Location | Purpose |
|---|---|
| [contracts/register-interface/](contracts/register-interface/README.md) | Proposed MMIO/descriptor tables, baseline comparison, source evidence and command examples for architecture#3. Keep the slide baseline unchanged; a proposal is not an accepted ABI. |
| [decisions/](decisions/README.md) | Accepted decisions and proposals using decision-template.md, with alternatives, supporting evidence and revisit conditions. |

## Current material and scope

The central diagram and small MAC example exist. The slide maps are preserved in docs/register-maps.md. The final accelerator ABI and compute partition are not decided.

[Shared diagram](https://github.com/SiliconBadgers/architecture/blob/main/docs/accelerator-diagram.md) · [Software evidence](https://github.com/SiliconBadgers/software/tree/main/experiments/llama-cpp/2026-09-22)

[CHARTER.md](CHARTER.md) and [OBJECTIVES.md](OBJECTIVES.md) describe the
longer-term purpose. Current issues and the starting guide specify the work
assigned now. [SETUP.md](SETUP.md) describes existing example commands and scope.
