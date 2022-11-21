# Designing a SIMD (vector) extension for a multicycle processor

|Item|Description|
|---|---|
|`ECE352_specific`| documentation|
|`multicycle_assembler`| assembler that takes test programs and compiles to memory data for simulation|
|`multicycle_documentation`| more documentation|
|`processor_v3_verilog`| verilog implementation of the processor to be modified|
|Project Overview Video|[https://www.youtube.com/watch?v=TWZiudul_ws](https://www.youtube.com/watch?v=TWZiudul_ws)|

## Steps to Assemble a Test Program

1) Run command `multicycle_assembler/asm.exe filename.s`.
2) Output file will be `multicycle_assembler/data.mif`.
3) Copy `data.mif.mem` to `processor_v3_verilog`.

## Steps to Simulate in Modelsim

1) Open `processor_v3_verilog` in ModelSim using `Change directory...`.
2) Run `do compile.do` to compile the `.v` files into ModelSim.
3) Run `do simulate.do data.mid.mem` to copy the program in `data.mid.mem` to the memory.
4) Run `do wave.do` to simulate some waveforms.
5) Run `run 10000ns` to run the processor for some time.

## Random Info

- 8-bit processor
- 4 registers, with 2-bit representations
- `ori imm` has implied register `k1` <- functions as `movi k1 imm`
- `nop` does nothing
- 256 bytes of memory

## What Have we Done?

1) add stop instruction `0001` to `FSM.v`
2) add stop state `c3_stop = 15` to `FSM.v`
3) add next stop state `c3_stop   state = c3_stop` <- it's a loop!
4) add stop controls, same as default
5) add a channel for the first bit in the instruction to check for stop/nop (in `multicycle.v`)
6) add a channel for the first bit in the instruction to check for stop/nop (in `FSM.v`)
7) add a switcher what the next state is for stop/nop
8) 

- in `multicycle.v` increase instruction width for FSM module
- in `FSM.v` increase instruction width
