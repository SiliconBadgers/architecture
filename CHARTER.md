# Architecture and system direction: team charter

Current assignments are listed in [docs/START-HERE.md](docs/START-HERE.md) and
the linked issues. The broader directions below provide context; they do not
replace those deliverables.

## Purpose

Help SiliconBadgers make coherent, evidence-based choices about the accelerator it is building. This team connects workload needs, numerical behavior, hardware organization and practical constraints so that separate teams can contribute to a system whose purpose and tradeoffs are understood.

Architecture gives shared meaning to work across the project. A locally effective compute block, memory system or software interface is useful when its assumptions fit the wider design. The team develops that common understanding and keeps alternatives and uncertainty visible as the project learns.

## Responsibilities

### System intent and tradeoffs

Develop and explain the relationship between intended workloads, capabilities, constraints and architectural choices. Maintain a system view that includes performance, storage, numerical behavior, programmability and implementation feasibility.

### Shared semantics

Steward the definitions that cross team boundaries: operations, data representations, interfaces, memory behavior and externally visible execution rules. Separate agreed behavior from open proposals and illustrative examples.

### Architectural reasoning

Use literature, analytical models, simulation, comparison studies and implementation feedback to examine alternatives. Document assumptions and explain where the available evidence supports a choice or leaves it uncertain.

### Continuity of understanding

Maintain accessible design explanations and decision rationale so new members can understand why the system has its current shape and can challenge those choices constructively.

## Boundaries and shared decisions

Architecture stewards shared specifications through discussion with the teams that implement and consume them. Compute, memory, control and SoC teams choose internal implementations within agreed boundaries. Software owns numerical references, workload mapping and software realization; accelerator maintains combined-system understanding and demonstrations. Architecture proposals become shared commitments through agreement with affected teams, not merely by appearing in this repository.

## Member autonomy

Members may choose an architectural question, compare competing organizations, examine workload needs, build a performance model, investigate a numerical format or improve an explanation. The team can decide its research methods and internal organization. Changes to shared semantics, resource assumptions or project-wide objectives need discussion with affected teams. A study that rules out a design can be a valuable result.

## Collaboration

| Partners | Shared concerns |
|---|---|
| software | Workload characteristics, numerical expectations and programming needs inform the system specification; architecture returns explicit assumptions and shared semantics. |
| RTL teams | Exchange resource and timing assumptions, interface proposals and feedback from implementation. Treat mismatches as opportunities to revise the shared design. |
| soc, physical-design and accelerator | Use platform constraints and measured system behavior to refine architectural claims and the interpretation of results. |

## Possible directions

Possible questions include how data reuse changes a memory hierarchy, where performance estimates depend on scheduling, which numerical assumptions matter for a workload, or how to explain an execution model to a new member. These are invitations to choose a direction, with no required sequence or predetermined answer.

## What progress means

Progress is visible when important assumptions become explicit, design choices can be explained, teams interpret shared behavior consistently and new evidence can change a decision. A well-supported comparison, a clarified contract or a reusable teaching note may be as valuable as a simulator.

Leads help members interpret this purpose, find collaborators, access resources
and share what they learn. Members choose their questions and contributions.
Research, design reasoning, experiments, implementation, documentation and
teaching can all advance the charter; success is not measured by the number of
code changes or completed tickets.

The team can revise this charter as its understanding evolves. Changes to a
shared boundary or commitment are discussed with the teams affected by them.
The [objectives](OBJECTIVES.md) describe durable outcomes, and the
[repository structure](README.md#repository-structure) provides places to develop
work without specifying a mandatory project or sequence.
