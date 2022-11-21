# Designing a SIMD (vector) extension for a multicycle processor

|Item|Description|
|---|---|
|`ECE352_specific`| documentation|
|`multicycle_assembler`| assembler that takes test programs and compiles to memory data for simulation|
|`multicycle_documentation`| more documentation|
|`processor_v3_verilog`| verilog implementation of the processor to be modified|
|Project Overview Video|[https://www.youtube.com/watch?v=TWZiudul_ws](https://www.youtube.com/watch?v=TWZiudul_ws)|

## Steps to Simulate in Modelsim

1) Run `do compile.do` to compile the `.v` files into ModelSim.
2) Run `do simulate.do data.mid.mem` to copy the program in `data.mid.mem` to the memory
3) Run `do wave.do` to simulate some waveforms.
4) Run `run 10000ns` to run the processor for some time.

## Random Info

- 8-bit processor
- 4 registers, with 2-bit representations
- `ori imm` has implied register `k1` <- functions as `movi k1 imm`
- `nop` does nothing
