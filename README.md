# ECE352 Project
> Designing a SIMD (vector) extension for a multicycle processor

## Useful Info

- `Ctrl-Shift-B` to "build" AKA assemble test programs into `data.mid` files.
- In ModelSim, `do go.do` to compile, load, waveform, and simulate the processor.
- `data.mid` files do not need to be moved!
- 8-bit processor with 256 bytes of memory
- 4 registers, with 2-bit representations, labelled k0 through k3
- [Project Overview Video](https://www.youtube.com/watch?v=TWZiudul_ws)
- To test a new assembly program on the board with no change to processor hardware, use `processor/UPDATE_MIF.bat`.

## Changes from Original

1) add stop instruction `0001` to `FSM.v`
2) add stop state `c3_stop = 15` to `FSM.v`
3) add next stop state `c3_stop   state = c3_stop` <- it's a loop!
4) add stop controls, same as default
5) add a channel for the first bit in the instruction to check for stop/nop (in `multicycle.v`)
6) add a channel for the first bit in the instruction to check for stop/nop (in `FSM.v`)
7) add a switcher what the next state is for stop/nop
8) 

## Instruction Set Architecture

- `IMM5`: 5-bit unsigned
- `IMM4`: 4-bit using 2's complement representation
- `IMM3`: 3-bit using sign/magnitude representation: `SMM`
     - `S=1` is positive
- `IMM2`: 2-bit unsigned
- EXT(`X`): sign-extend `X` to 8 bits
     - eg: 101 = 5; EXT(101) = 00000101
     - eg: 1101 = -3; EXT(1101) = 11111101
- `ka`, `kb`: registers variables
     - encoded as 2 bits
- `~`: immediate value encoded as bits
- *: Z = (`result` == 0), N = (`result` < 0)
     - this is true for arithmetic operations

Instruction|Action|Encoding<br>[MSB]76543210[LSB]
---|---|---
LOAD `ka` (`kb`)|`ka` ← MEM[`kb`]|`kakb0000`
STORE `ka` (`kb`)|MEM[`kb`] ← `ka`|`kakb0010`
*ADD `ka` `kb`|`ka` ← `ka` + `kb`|`kakb0100`
*SUB `ka` `kb`|`ka` ← `ka` - `kb`|`kakb0110`
*NAND `ka` `kb`| `ka` ← ! ( `ka` & `kb` )|`kakb1000`
*ORI `IMM5`|`k1` ← `k1` \| `IMM5`|`~~~~~111`
*SHIFT `ka` `IMM3`|`ka` = `ka` << `IMM3`|`ka~~~011`
*SHIFTL `ka` `IMM2`|`ka` = `ka` << `IMM2`|`ka1~~011`
*SHIFTR `ka` `IMM2`|`ka` = `ka` >> `IMM2`|`ka0~~011`
BZ `IMM4`|IF (`Z` == 1) `PC` ← `PC` + EXT(`IMM4`)|`~~~~0101`
BNZ `IMM4`|IF (`Z` == 0) `PC` ← `PC` + EXT(`IMM4`)|`~~~~1001`
BPZ `IMM4`|IF (`N` == 0) `PC` ← `PC` + EXT(`IMM4`)|`~~~~1101`
STOP|`PC` ← `PC` - 1|`00000001`
NOP|nothing lol|`10000001`
