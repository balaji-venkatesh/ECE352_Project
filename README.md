# Designing a SIMD (vector) extension for a multicycle processor



## Useful Scripts in this Workspace

- `Ctrl-Shift-B` to "build" AKA assemble test programs into processor memory.
- In ModelSim, `do go.do` to compile, load, waveform, and simulate the processor.

## Random Info

- 8-bit processor
- 4 registers, with 2-bit representations
- `ori imm` has implied register `k1` <- functions as `movi k1 imm`
- `nop` does nothing
- 256 bytes of memory
- [Project Overview Video](https://www.youtube.com/watch?v=TWZiudul_ws)

## Help What Have we Done?

1) add stop instruction `0001` to `FSM.v`
2) add stop state `c3_stop = 15` to `FSM.v`
3) add next stop state `c3_stop   state = c3_stop` <- it's a loop!
4) add stop controls, same as default
5) add a channel for the first bit in the instruction to check for stop/nop (in `multicycle.v`)
6) add a channel for the first bit in the instruction to check for stop/nop (in `FSM.v`)
7) add a switcher what the next state is for stop/nop
8) 


## Assembler Info


7. If you haven't changed anything about your processor hardware, but want to test a new assembly program on the board  you can update and download your system with a new *.mif file by clicking on the 'UPDATE_MIF.bat' batch file in the Quartus project folder. It is much faster than re-starting the whole Quartus compile. Alternatively, you can call it directly after assembling from the NIOS II console with
	> cmd /C UPDATE_MIF.bat
	
REMEMBER: If you try out hardware changes, SIMULATE them first before trying them on the board. Much easier and faster to debug.



## Instruction Set Architechture Documentation

- IMM3 is a 3-bit immediate using sign/magnitude representation:
     - bit 2 = sign, value = bits 1 and 0
- IMM4: 4-bit immed using 2's complement representation
- IMM5: 5-bit unsigned
- EXT(X): sign-extend X to 8 bits
     - eg: 101 = 5; EXT(101) = 00000101
     - eg: 1101 = -3; EXT(1101) = 11111101
- R1, R2: registers variables
- TMP = temporary variable
- Instruction Encodings:
     - Rx = 2 bit encoding of register
     - I  = immediate value
     - Bit [MSB]76543210[LSB]



|Instruction|Action|Encoding|
|---|---|---|
|LOAD R1 (R2)|R1 = MEM[`R2`]|R1R20000|
|STORE R1 (R2)|MEM[`R2`] = `R1`|R1R20010|
|ADD R1 R2|`R1` = `R1` + `R2`|R1R20100
||IF (`R1` + `R2` == 0) Z = 1; ELSE Z = 0;
||IF (`R1` + `R2` < 0) N = 1; ELSE N = 0;
|SUB R1 R2|`R1` = `R1` - `R2`|R1R20110
||IF (`R1` - `R2` == 0) Z = 1; ELSE Z = 0;
||IF (`R1` - `R2` < 0) N = 1; ELSE N = 0;
|NAND R1 R2| `R1` = ! ( `R1` & `R2` )|R1R21000
||IF ( ! ( `R1` & `R2` ) == 0) Z = 1; ELSE Z = 0;
||IF ( ! ( `R1` & `R2` ) < 0) N = 1; ELSE N = 0;
|ORI IMM5|`K1` = `K1` bitwise-OR IMM5|IIIII111
||IF (TMP == 0) Z = 1; ELSE Z = 0;
||IF (TMP < 0) N = 1; ELSE N = 0;
|SHIFT R1 IMM3|IF (IMM3 > 0) `R1` = `R1` << IMM3; ELSE `R1` = `R1` >> (-IMM3)|R1III011
||IF (TMP == 0) Z = 1; ELSE Z = 0;
||IF (TMP < 0) N = 1; ELSE N = 0;
|BZ IMM4|IF (Z == 1) PC = `PC` + EXT(IMM4)|IIII0101
|BNZ IMM4|IF (Z == 0) PC = `PC` + EXT(IMM4)|IIII1001
|BPZ IMM4|IF (N == 0) PC = `PC` + EXT(IMM4)|IIII1101
|STOP||00000001
|NOP||00001010
```

## How to Change the .mif Filename

To change the *.mif file that is used to initialize the instruction 
memory in Quartus, open either DataMemory.v (for the original RAM) or 
DualMem.v (for the Dualport RAM) and look for the line that contains
altsyncram_component.init_file = ...
                   