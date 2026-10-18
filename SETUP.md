# architecture: optional example setup

No tools are required to read the charter or contribute research and design
material. The commands below apply only to the existing technical example.

## Existing example

A small signed-MAC contract and a structural JSON check are present. The contract describes that example; it does not define a complete accelerator architecture.

Prerequisites: Make and [uv](https://docs.astral.sh/uv/getting-started/installation/)
0.12.23 or newer. uv uses an available Python 3.11+ interpreter or downloads a
compatible one when needed. The current example uses the standard library;
`make setup` creates the locked `.venv` without third-party packages.
Keep the component folders as siblings for the provided cross-component paths.

From this component directory:

```sh
make setup
make doctor
make test
```

These commands check the current example files. The combined MAC example can be
run from the sibling `accelerator` folder using the same commands. It exercises
four model tests, 261 reference vectors and 131,600 RTL checks. It establishes
no full-accelerator, board or physical-implementation claim.

Run `make clean` from `accelerator` to remove generated build outputs and Python
caches before sharing a folder snapshot. The runner reads the current sibling
files and does not create commits.

## Example files

- [contracts/mac-v0.json](contracts/mac-v0.json)

For the shared example, see the [workspace checkout guide](https://github.com/SiliconBadgers/soc/blob/main/docs/GETTING_STARTED.md).

## Reproduce historical plots with uv

The vector-control study keeps its original requirements, inputs and results.
To render its figures with that same pinned matplotlib requirement, run from
the repository root:

```sh
uv run --locked --group vector-plots python research/2026-10-02-vector-control/plot.py
```

The optional `vector-plots` group preserves `matplotlib==3.11.2` from the dated
requirements and locks its transitive dependencies in `uv.lock`. The example
checks require only the standard library; `make setup` syncs the environment
without the optional plotting packages. The rendering
command regenerates figures in the study directory; review those files before
committing. The original study requirements, results and inputs are unchanged.
