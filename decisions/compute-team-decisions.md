# Compute team decisions

- Matrix unit decisions
  - The matrix unit supports matrix–matrix multiplication, matrix–vector
    multiplication, and vector outer products.
  - Stationary output will be supported. The unit will have an input controlling whether to write the output or to keep it in the accumulators.

- Vector unit decisions
  - The vector unit handles element-wise operations, reductions, conversions,
    and activation/normalization kernels.
  - Firmware supplies kernels such as softmax, sigmoid, SiLU, and ReLU.
  - SIMD primitives include arithmetic, shifts, conversions, SUM/MIN/MAX
    reductions, integer square root, and floating-point exponent and reciprocal
    square root.
  - ARGMAX and absolute-max are programs composed from SIMD primitives.
  - See the [SIMD ISA](https://github.com/SiliconBadgers/rtl/blob/main/docs/simd-isa.md)
    for the command format and execution rules, and the
    [signature catalogue](https://github.com/SiliconBadgers/rtl/blob/main/docs/simd-isa-signatures.md)
    for supported operations and operand types.

- Command sequencing decisions
  - SIMD commands use a fixed 32-bit format.
  - The device-side RISC-V core submits commands to the sequencer, which
    dispatches work to the matrix and vector units.
  - A local RISC-V core will issue SIMD primitives; the SIMD array has no
    control flow of its own.

- Datatype decisions (initial implementation direction)
  - Model-wide numerical validation is tracked in
    [architecture #9](https://github.com/SiliconBadgers/architecture/issues/9).
  - Weights: signed INT4 or INT8 with block and per-tensor scales.
  - Activations: INT8. Ordinary matrix accumulation: INT32, then requantize to
    INT8.
  - Q/K: INT16 blocks sharing an exponent. Whether these values stay entirely
    inside the vector unit still needs confirmation.
  - Gated DeltaNet decay math: Q8.24 fixed point to preserve small decay terms.
  - Vector arithmetic and conversion operand types follow the SIMD signature
    catalogue. Vector kernels dequantize, compute in floating point where needed,
    then requantize.
