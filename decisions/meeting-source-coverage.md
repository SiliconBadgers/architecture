# Meeting sources for the open-decision register

This index maps the September 27–October 12, 2026 meeting-note snapshot to
[decision IDs](open-decisions.md). It records technical evidence and its date;
a later decision or implementation review can supersede an earlier proposal.
Notion links may require team access. Scheduling and availability records do
not establish technical decisions and are excluded.

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

## Interpretation

The merged compute decisions and SIMD ISA take precedence over older candidates.
October 4 defers dedicated recurrence hardware and an LLVM backend; October 12's
semester simulation goal supersedes October 6's semester FPGA goal. Numerical
examples in meeting notes are not approved sweep bounds. Meeting summaries and
captions are supporting sources, not independently verified recordings.
