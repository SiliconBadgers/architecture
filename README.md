# Architecture and system direction

## Shared block diagram

The [main accelerator diagram](docs/accelerator-diagram.md) is the central reference for all teams. Its four compute boxes are provisional: Compute will research the required units using the Software evidence, while Control and Memory develop detailed diagrams for their respective controllers.

Help SiliconBadgers make coherent, evidence-based choices about the accelerator it is building. This team connects workload needs, numerical behavior, hardware organization and practical constraints so that separate teams can contribute to a system whose purpose and tradeoffs are understood.

## Register and descriptor maps

The [two maps from the technical deck](docs/register-maps.md) preserve the proposed
MMIO registers and 128-byte command descriptor. Top-Level Control will refine
these in this repository using llama.cpp and Software's evidence, while keeping
its detailed controller diagram and command walkthrough in
[rtl-control](https://github.com/SiliconBadgers/rtl-control/issues/2).

## Read the charter

- [CHARTER.md](CHARTER.md): purpose, responsibilities, boundaries, member autonomy and collaboration.
- [OBJECTIVES.md](OBJECTIVES.md): high-level outcomes that members can choose how to advance.
- [SETUP.md](SETUP.md): optional technical setup and the scope of any existing example.

## Choosing a contribution

Members choose their work in conversation with the charter and their interests.
A contribution can be a research question, a design study, an experiment, an
implementation, a useful explanation or teaching material. Leads help connect
people, questions and evidence. Shared interfaces and commitments are discussed
with the teams that depend on them.

The scaffold supplies places for that work. It does not specify a backlog,
required first project, milestone sequence or personal assignment.

## Repository structure

| Location | Purpose |
|---|---|
| [docs/](docs/README.md) | Design explanations, proposals, reviews, decisions and learning material. Let the content evolve with the team’s questions; link research and experiment evidence where useful. |
| [research/](research/README.md) | Literature notes, surveys, analytical studies and comparisons relevant to the charter. Explain the question, sources, interpretation and remaining uncertainty in a form that suits the work. |
| [experiments/](experiments/README.md) | Exploratory studies, prototypes and experiment narratives. Make the question and interpretation understandable; preserve the context needed to revisit a result. These artifacts need not be production implementations. |
| [contracts/](contracts/README.md) | Shared interface and numerical definitions, clearly distinguishing accepted project agreements from examples or proposals. |
| [decisions/](decisions/README.md) | Architectural decision rationale, alternatives, assumptions and the perspectives of affected teams. |

The team may extend this structure as useful. Existing example entry points stay
in their current locations, described in [SETUP.md](SETUP.md).

## Current material

A small signed-MAC contract and a structural JSON check are present. The contract describes that example; it does not define a complete accelerator architecture.

Existing code is optional material for learning or experimentation. Its behavior
and tests describe that example and do not select the team’s future design.
Reading or contributing to the charter, research and design documentation needs
no tool installation.

This is the [SiliconBadgers/architecture](https://github.com/SiliconBadgers/architecture) team repository.
The [organization guide](https://github.com/SiliconBadgers/accelerator/blob/main/docs/TEAM_GUIDE.md)
and [repository map](https://github.com/SiliconBadgers/accelerator/blob/main/docs/REPOSITORIES.md)
explain how the teams connect.
