# Shared workload cases

Status: source evidence plus proposed study cases, September 22, 2026.

## Recorded workload

The committed [Software experiment](https://github.com/SiliconBadgers/software/tree/cc846ec/experiments/llama-cpp/2026-09-22)
uses Qwen3.5-2B Q4_K_M, llama.cpp `f46bc30cb6a7f68a67e34a00061e20a4ad1eff43`,
one sequence, six CPU threads and a repeated passage. Prompt lengths are 128,
512, 2048 and 8192, followed by 32 teacher-forced decode steps. CPU and Metal
baselines have three repetitions. This is a performance probe, not task quality.

Use [manifest.json](https://github.com/SiliconBadgers/software/blob/cc846ec/experiments/llama-cpp/2026-09-22/manifest.json)
for model revision/hash, context allocation and instrumentation exclusions.
Physical prefill microbatches are capped at 512; distinguish a logical 2048-token
prompt from the matrices in each actual graph invocation. The anomalous 8192-token
instrumented timing is excluded from performance conclusions.

## Matrix input facts

[matrix-cases.csv](matrix-cases.csv) is a nine-row selection from the committed
[matrix inventory](https://github.com/SiliconBadgers/software/blob/cc846ec/experiments/llama-cpp/2026-09-22/results/matrix-weight-inventory.json).
Source SHA256: `8d5acd97f8326f673ea13850b06ebc5d9620f4e99e77c24fd0b2ee251aa3f97b`.
The columns preserve ggml's dimension order: `ne0` is the matrix reduction width
and `ne1` the output-channel count for these matrix weights. These are not C-array
row/column declarations or a hardware storage layout. Bytes include the recorded
GGUF block encoding; they are not measured bus/DRAM traffic.

`token_embd.weight` is reused for the vocabulary output projection in this model;
do not count an invented separate output weight array. The 417,177,600-byte Q6_K
matrix deserves an explicit residency/streaming study. GGUF formats differ
between selected tensors and even between similar layers.

## Initial studies using those facts

| Case | Starting point | Compare / expose |
|---|---|---|
| Single-token projection | Selected projection weights, one input column | Lane utilization, weight traffic, partial sums and tails |
| Prefill projection | Same weights, 128 and 512 input columns as study points | Tiling/reuse and activation/output working set |
| Output head | Tied embedding matrix, one scored token | Weight residency, arithmetic reuse and cost of producing logits |
| Full attention | Saved shapes/traces for attention layers | QK/softmax/AV dependencies, KV state and context scaling |
| DeltaNet/convolution | Saved shapes/traces for recurrent layers | Update/read ordering, persistent state and convolution history |
| Command/transfer fault | Synthetic variable-latency engine/memory stubs | Outstanding work, buffer ownership, drain and completion visibility |

The input-column counts above are comparison cases, not a claim that every
operation processes every prompt token identically. Inspect the actual graph
trace, especially the output head. For stateful operations, use the full
[compressed shape inventory](https://github.com/SiliconBadgers/software/blob/cc846ec/experiments/llama-cpp/2026-09-22/results/operator-shapes.json.gz)
and [analysis procedure](https://github.com/SiliconBadgers/software/blob/main/experiments/llama-cpp/2026-09-22/README.md)
rather than inventing state dimensions from matrix weights.

For new results record: case, source revision, format, dimensions/strides,
sequence/context, assumptions, method, units, numerical check and limitations.
Each team can start with these cases and publish refinements independently.
