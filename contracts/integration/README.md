# Provisional integration types

`command_pkg.sv` is the shared command/completion type package for the RTL
integration experiment. It is a routing subset, not an accepted device ABI.
ABI 1, error encodings and the vector/state/memory test opcodes are provisional.
The package contains no datapath implementation and does not replace the
[register-interface proposal](../register-interface/README.md).

The consolidated [accelerator workspace](https://github.com/SiliconBadgers/soc)
pins this repository as a submodule and compiles the package before its consumers.
Changing these types requires coordinated consumer tests in Control, Software
and Verification. The four test routes do not select a physical compute partition.
