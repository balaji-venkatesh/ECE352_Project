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

## Compiler Info
```
You can compile and use the assembler for the multicycle processor in the NIOS II Cygwin console, which gives you a Linux shell environment:
1.	Open Start->All Programs->Altera 11.1...->Nios II EDS...->NIOS II Command Shell
2.  You can reach your W:\ directory with 
		> cd /cygdrive/w/
	and other Windows paths in similar fashion
3.	Go to the path holding the asm.cpp source and type
		> make
4. You can now assemble files by calling
		> ./asm YOURCODE.s
5. The assembler will produce a file 'data.mif' to use for inclusion in your Quartus bitstream, and a file 'data.mif.mem' that is used for ModelSim simulation
6. You can either copy the two files into your Quartus project folder, or copy the asm.exe file into your project folder and build the files right there, whatever you preference is
7. If you haven't changed anything about your processor hardware, but want to test a new assembly program on the board  you can update and download your system with a new *.mif file by clicking on the 'UPDATE_MIF.bat' batch file in the Quartus project folder. It is much faster than re-starting the whole Quartus compile. Alternatively, you can call it directly after assembling from the NIOS II console with
	> cmd /C UPDATE_MIF.bat
	
REMEMBER: If you try out hardware changes, SIMULATE them first before trying them on the board. Much easier and faster to debug.
```


## Instruction Set Architechture Documentation

```
NOTES:
* IMM3 is a 3-bit immediate using sign/magnitude representation:
  * bit 2 = sign, value = bits 1 and 0
* IMM4: 4-bit immed using 2's complement representation
* IMM5: 5-bit unsigned
* EXT(X): sign-extend X to 8 bits
  * eg: 101 = 5; EXT(101) = 00000101
  * eg: 1101 = -3; EXT(1101) = 11111101
* R1, R2: registers variables
* TMP = temporary variable

Register Transfer Notation:

LOAD R1 (R2):
     TMP = MEM[[R2]]
     R1 = TMP
     [PC] = [PC] + 1

STORE R1 (R2):
     MEM[[R2]] = [R1]
     [PC] = [PC] + 1

ADD R1 R2
     TMP = [R1] + [R2]
     R1 = TMP
     IF (TMP == 0) Z = 1; ELSE Z = 0;
     IF (TMP < 0) N = 1; ELSE N = 0;
     [PC] = [PC] + 1

SUB R1 R2
     TMP = [R1] - [R2]
     R1 = TMP
     IF (TMP == 0) Z = 1; ELSE Z = 0;
     IF (TMP < 0) N = 1; ELSE N = 0;
     [PC] = [PC] + 1

NAND R1 R2
     TMP = [R1] bitwise-NAND [R2]
     R1 = TMP
     IF (TMP == 0) Z = 1; ELSE Z = 0;
     IF (TMP < 0) N = 1; ELSE N = 0;
     [PC] = [PC] + 1

ORI IMM5
    TMP = [K1] bitwise-OR IMM5
    [K1] = TMP
    IF (TMP == 0) Z = 1; ELSE Z = 0;
    IF (TMP < 0) N = 1; ELSE N = 0;
    [PC] = [PC] + 1

SHIFT R1 IMM3
    IF (IMM3 > 0) TMP = [R1] << IMM3
    ELSE TMP = [R1] >> (-IMM3)
    R1 = TMP
    IF (TMP == 0) Z = 1; ELSE Z = 0;
    IF (TMP < 0) N = 1; ELSE N = 0;
    [PC] = [PC] + 1

BZ IMM4
     IF (Z == 1) PC = [PC] + EXT(IMM4)
     [PC] = [PC] + 1

BNZ IMM4
     IF (Z == 0) PC = [PC] + EXT(IMM4)
     [PC] = [PC] + 1

BPZ IMM4
     IF (N == 0) PC = [PC] + EXT(IMM4)
     [PC] = [PC] + 1


Instruction Encodings:
Legend:
Rx = 2 bit encoding of register
I  = immediate value

Bit [MSB]76543210[LSB]

LOAD:    R1R20000
STORE:	 R1R20010
ADD:	 R1R20100
SUB:	 R1R20110
NAND:	 R1R21000
ORI:	 IIIII111
SHIFT:	 R1III011
BZ:	 IIII0101
BNZ:	 IIII1001
BPZ:	 IIII1101

STOP:	 00000001
NOP:	 00001010

```

## How to Change the .mif Filename

To change the *.mif file that is used to initialize the instruction 
memory in Quartus, open either DataMemory.v (for the original RAM) or 
DualMem.v (for the Dualport RAM) and look for the line that contains
altsyncram_component.init_file = ...
