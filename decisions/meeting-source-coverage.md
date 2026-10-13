# Meeting-source coverage for the open-decision register

Snapshot checked: **October 13, 2026 UTC**. Companion to the
[open-decision register](open-decisions.md); IDs below refer to that document.

This pass fetched all **38 pages** returned by the accessible Notion **Meeting
notes** database (unfiltered query exhausted; no further page): **12 completed/Ready notes**, **19 scheduled entries**, and
**7 availability/planning entries**. This bounds the claim: it is not a crawl of
every document, slide, attachment or unrelated page in the Notion workspace.
The first PR version used only six recent completed meeting notes; this manifest
records the expanded review and the older evidence reconciled into it.

Meeting dates below use **America/Chicago**, matching the meeting notes.
Source revision times are the last-edited timestamps returned by Notion, in UTC.
Notes summarize discussion rather than certify an implementation or acceptance.
Sources may require team access; each substantive open question is restated in
the register, without copying recordings, credentials or restricted collateral.

## Completed meeting notes reviewed

| Meeting / source | Source last edited (UTC) | Contribution and later-source reconciliation |
|---|---|---|
| [Sep 27 · Software Subteam Meeting](https://app.notion.com/3e938826be1b81ee9c55dd9b4909151b) | 2026-10-11T18:28:07.678Z | C01/C07, M02/M09, T01/T10, S01–S03, P01/P03. Early dedicated-recurrence option narrowed by Oct 4; about 32×32 was exploratory. |
| [Sep 28 · SB Tech Weekly Sync](https://app.notion.com/3e938826be1b810889c4f4a0b672ccad) | 2026-10-07T03:37:24.765Z | Shared SRAM and retained RISC-V baseline; M02/M07, T01, N01, P01/P03. Early FP4-vs-integer question narrowed by the merged compute direction; roughly 1 mm² was a discussed planning assumption, not measured area or a selected tapeout. |
| [Oct 03 · Compute Subteam Meeting](https://app.notion.com/3ee38826be1b81668497e19a4ea5994f) | 2026-10-05T17:54:09.361Z | C01/C02/C06, V06, P03. Adds PE carry-save comparison and deferred DFT. Scale-per-16 and packed-product ideas remain proposals under later provisional-scale notes; early ISA/register/control candidates defer to published ISA. |
| [Oct 04 · Software Subteam Meeting](https://app.notion.com/3ee38826be1b81a2befbcb825ed98b95) | 2026-10-11T17:54:31.772Z | C07 no dedicated recurrence unit for now; N04/S02 shared dependency graph; T01 handwritten activation programs, no LLVM backend needed for now. Later merged Software baseline supersedes cleanup requests as pending implementation work. |
| [Oct 05 · Verification Subteam Meeting](https://app.notion.com/3f138826be1b81b58ff4f5e654488270) | 2026-10-07T03:37:16.820Z | V01–V03/V05 subsystem boundaries, independent checking and testbench/repository arrangements. Distinguishes toy PE onboarding from real verification; later Oct 12 assignments/build discussion takes precedence. |
| [Oct 05 · SB Tech Weekly Sync](https://app.notion.com/3f238826be1b81c6ac8fed789f1b655f) | 2026-10-07T01:49:08.962Z | V04/V05 protocol versions and smoke/full regression/runner split; P04–P06 tools, target-specific sign-off, PDK storage/co-location and memory/PLL exploration. Top-level/memory Controller merger was already settled, not an open architectural choice. |
| [Oct 06 · Controller Subteam Meeting · Oct 6](https://app.notion.com/3f238826be1b81ff9d04d4f927a5a3fd) | 2026-10-07T03:37:19.344Z | M03/M06–M09, T05, V02; HBM interface/concurrency, bank layout, dependencies and shared build. Suggested owners and dates are not final specifications. |
| [Oct 06 · Physical Design Subteam Meeting](https://app.notion.com/3f238826be1b8118970bfcbfebf82052) | 2026-10-07T08:55:43.327Z | P02 constrained flow and trustworthy feedback. Primarily an educational flow overview; not every flow stage is a new architecture decision. Semester FPGA goal superseded by Oct 12. |
| [Oct 10 · Compute Subteam Meeting](https://app.notion.com/3f538826be1b81e1a8e0d468ad655828) | 2026-10-10T23:28:54.926Z | C01–C06, M01/M03/M08, P01/P03; confirms 32-bit width, open physical vector/memory sizing and wrapper ownership. Stationary-output support subsequently recorded in merged compute decisions. |
| [Oct 11 · Software Subteam Meeting](https://app.notion.com/3f638826be1b816d957ee6404acd16cf) | 2026-10-11T22:53:00.227Z | C02, M01, N04, S01–S03, P01; provisional scaling/outer-product type, simulator scope/calibration and common graph baseline. No overall freeze date or numeric team sweep bounds established. |
| [Oct 12 · Verification Subteam Meeting](https://app.notion.com/3f838826be1b815f84daede3314f6389) | 2026-10-13T03:31:33.856Z | M07, V01–V03; DMA role, subsystem boundaries and traceable test planning. Scheduled diagram targets are not evidence of completion. |
| [Oct 12 · SB Tech Weekly Sync](https://app.notion.com/3f838826be1b813b8654e35c9dce4bd7) | 2026-10-13T03:17:48.862Z | M08, T05, V01/V02, P01; command/HBM dependencies and unresolved shared build. Simulation-token semester goal is agreed; early-next-semester FPGA remains proposed; FPGA/tapeout scope unresolved. |

## Scheduled entries fetched and classified

These pages contained scheduling information rather than substantive completed
meeting notes in this snapshot. A scheduled entry is not a second meeting or
proof that a meeting occurred. Several coexist with a separate completed/Ready
page above; they are not double-counted as architecture evidence.

In particular, **October 13 Controller has a page but no actual meeting notes**
to incorporate yet. October 13 Physical Design is also scheduled-only here.

| Meeting date (Central) / source | Classification |
|---|---|
| [2026-10-05 · Verification Subteam Meeting](https://app.notion.com/3ee38826be1b8149a28dd00462c2abb3) | Scheduled metadata; no completed notes. |
| [2026-10-05 · SB Tech Weekly Sync](https://app.notion.com/3e938826be1b81ed9dd8da63512c5f35) | Scheduled metadata; no completed notes. |
| [2026-10-06 · Controller Subteam Meeting](https://app.notion.com/3ee38826be1b8150976cdef101653f48) | Scheduled metadata; no completed notes. |
| [2026-10-06 · Physical Design Subteam Meeting](https://app.notion.com/3ee38826be1b81d3bc0bf1222bcffa29) | Scheduled metadata; no completed notes. |
| [2026-10-10 · Compute Subteam Meeting](https://app.notion.com/3ee38826be1b815fade3c4a85aafb3cf) | Scheduled metadata; no completed notes. |
| [2026-10-11 · Software Subteam Meeting](https://app.notion.com/3ee38826be1b816cbf57eabb4a96b302) | Scheduled metadata; no completed notes. |
| [2026-10-12 · Verification Subteam Meeting](https://app.notion.com/3ee38826be1b81db81aded8f2795d444) | Scheduled metadata; no completed notes. |
| [2026-10-12 · SB Tech Weekly Sync](https://app.notion.com/3e938826be1b8185be92d5d0ae740f02) | Scheduled metadata; no completed notes. |
| [2026-10-13 · Controller Subteam Meeting](https://app.notion.com/3ee38826be1b81d7a054f148633ad199) | Scheduled metadata; no completed notes. |
| [2026-10-13 · Physical Design Subteam Meeting](https://app.notion.com/3ee38826be1b81e98e70efd395df43df) | Scheduled metadata; no completed notes. |
| [2026-10-17 · Compute Subteam Meeting](https://app.notion.com/3ee38826be1b81c997b8ff755ca3882e) | Scheduled metadata; no completed notes. |
| [2026-10-18 · Software Subteam Meeting](https://app.notion.com/3ef38826be1b8158bb3fd6ff5b0afc4b) | Scheduled metadata; no completed notes. |
| [2026-10-19 · SB Tech Weekly Sync](https://app.notion.com/3e938826be1b81da9beed0deed337889) | Scheduled metadata; no completed notes. |
| [2026-10-26 · SB Tech Weekly Sync](https://app.notion.com/3e938826be1b81f7a1a4e0a4e669106d) | Scheduled metadata; no completed notes. |
| [2026-11-02 · SB Tech Weekly Sync](https://app.notion.com/3e938826be1b81a1ae48c66e38aa87dc) | Scheduled metadata; no completed notes. |
| [2026-11-09 · SB Tech Weekly Sync](https://app.notion.com/3ea38826be1b810693acf463aab205ca) | Scheduled metadata; no completed notes. |
| [2026-11-16 · SB Tech Weekly Sync](https://app.notion.com/3ea38826be1b81329c59c7b47cfc4af9) | Scheduled metadata; no completed notes. |
| [2026-11-23 · SB Tech Weekly Sync](https://app.notion.com/3ea38826be1b813cb704e377ff1d7417) | Scheduled metadata; no completed notes. |
| [2026-11-30 · SB Tech Weekly Sync](https://app.notion.com/3ea38826be1b8138817df1ccb7b2e247) | Scheduled metadata; no completed notes. |

## Availability/planning entries fetched and classified

No architectural decisions were drawn from these undated availability pages.
Some are historical/deleted page records still returned by the database.

- [Historical planning — Software meeting availability](https://app.notion.com/1d01771fbe744f1392707c627ba1d8e6)
- [Historical planning — Memory Control meeting availability](https://app.notion.com/1d5508945b19442d92744c1121cff29e)
- [Historical planning — Physical Design meeting availability](https://app.notion.com/25ee1251005e41eb82492b582baf1b7f)
- [Compute 1 meeting availability](https://app.notion.com/6b0ca628fc91471aa11d409fcefa091a)
- [Historical planning — Compute 2 meeting availability](https://app.notion.com/97f7dbcdeb9f48be952c8eefe083b76b)
- [Historical planning — Verification meeting availability](https://app.notion.com/c6c400749142483696a6fdabe893edd5)
- [Historical planning — Top-Level Control meeting availability](https://app.notion.com/f272f21b403b4c2cbb40d0879d4bc920)

## Supplemental stored Notion captions

The two transcript index pages and all seven stored child caption parts were
also fetched and read in full. They supplied no additional open-decision family
or superseding agreement; their static/dynamic mapping, conditional clock-domain
crossing and historical workload-target details refine T01, P03 and N04. Automatic captions can misstate
words or speakers; they are not independently checked recordings.

- [Software Sep 27 transcript index](https://app.notion.com/p/3e938826be1b81efb493f5bc9ecbbfc1): [part 1](https://app.notion.com/p/3e938826be1b8119a77bfe9640743d0f), [part 2](https://app.notion.com/p/3e938826be1b8191a268d2c4df8df4aa), [part 3](https://app.notion.com/p/3e938826be1b81e9b945dec611a425e4), [part 4](https://app.notion.com/p/3e938826be1b81f4b98bd8ba3ff132dd)
- [Tech Sync Sep 28 transcript index](https://app.notion.com/p/3ea38826be1b81739835d18f3a998c9a): [part 1](https://app.notion.com/p/3ea38826be1b81e789b9f5f411524696), [part 2](https://app.notion.com/p/3ea38826be1b8100835cc1b4f57a85e0), [part 3](https://app.notion.com/p/3ea38826be1b8188ba98f7d50d5e726b)

Historical availability pages mention September 25–26 meetings, but no substantive
notes for those meetings were present among the returned database pages. Those
meetings are not claimed as reviewed.

## Precedence and remaining limits

- Keep later source decisions: the merged compute record and SIMD ISA constrain
  older candidates; Oct 4 defers a dedicated recurrence unit and an LLVM backend;
  Oct 12's semester simulation goal supersedes Oct 6's semester FPGA goal.
- Quantitative examples in meetings are not sweep bounds. Scale-per-16, 32×32
  arrays, about 40 MB FPGA SRAM, roughly 1 mm² shuttle area and five-minute CI
  were described in context; none is promoted into a newly approved range.
- The register retains exact historical GitHub sweep grids with their model
  provenance. No meeting note supplied an agreed new min/max/step grid.
- Scheduling/onboarding/recruiting/funding logistics are not converted into
  hardware parameters. Tool, IP, verification and PDK access constraints are
  included where they affect implementation or trustworthy evidence.
- Current Discord access remains partial as documented in the register. The
  database snapshot cannot establish newer agreements absent from its notes.
- Linked recordings and slide/file attachments were not independently watched
  or comprehensively inspected in this pass. Later notes and implementation
  reviews may still resolve, add or narrow decisions.
