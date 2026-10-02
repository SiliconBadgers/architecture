# Captured study inputs

These snapshots freeze the inputs used by the October 2 vector-control study. They contain model metadata and analytical code, not model weights or compiled dependencies. The experiment's `results.json` records their exact SHA-256 digests.

| File | Origin and use |
|---|---|
| `graph-data.js` | Byte-identical to the [Software explorer graph](https://github.com/SiliconBadgers/software/blob/11d36ed81180607cd98e61151a403f5256eaf13b/experiments/llama-cpp/2026-09-24-qwen35-2b/explorer/graph-data.js). Captured graph provenance is preserved by the [original import record](https://github.com/SiliconBadgers/software/blob/11d36ed81180607cd98e61151a403f5256eaf13b/experiments/llama-cpp/2026-09-24-qwen35-2b/IMPORT.md). |
| `engine.js` | Derived from the [Software analytical engine](https://github.com/SiliconBadgers/software/blob/11d36ed81180607cd98e61151a403f5256eaf13b/experiments/llama-cpp/2026-09-24-qwen35-2b/explorer/engine.js), with the local changes described below. |
| `2B.json` | Previously captured [Qwen3.5-2B configuration](https://huggingface.co/Qwen/Qwen3.5-2B/blob/main/config.json). The capture recorded a content hash, not an immutable upstream revision; use this included snapshot for reproduction. |
| `architecture.cjs` | Configuration-to-dimension helper from the local Qwen-family study. Only `architecture()` is used here. Its synthetic graph generator and parameter counter are retained as part of the frozen snapshot but are not used for the reported results. |

## Engine changes relative to Software

The upstream engine SHA-256 was `8174a7bdf558365d1cf2453266097c3dabe64974c9c7e0912dad9f36f11d7dd2`. This snapshot replaces hard-coded state/cache dimensions with fields derived from the model configuration, adds optional local-state service accounting, and exposes per-node read/write/spill quantities. The optional recurrence-local-storage path is disabled in this study. Dedicated recurrence count is zero.

The vector-controller model in `../model.cjs` is separate from this inherited engine. `../run.cjs` uses the inherited engine only for the exploratory whole-graph projection and retains its unsupported-node and HBM timings. The reference kernel sweeps do not depend on that projection. The original engine equations and limitations are documented in [Software MODEL.md](https://github.com/SiliconBadgers/software/blob/11d36ed81180607cd98e61151a403f5256eaf13b/experiments/llama-cpp/2026-09-24-qwen35-2b/explorer/MODEL.md).

## Attribution

Zeb Taylor's QwenProfiling project is the source of the captured graph and original explorer imported into Software. The existing import record remains authoritative for its history. Local extensions and the new vector-control study were prepared with OpenAI Codex. The publication session reports `gpt-6-astra` through Git AI; this does not retroactively attribute the captured inputs or earlier local experiments to that model.
