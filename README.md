# Designing a SIMD (vector) extension for a multicycle processor

[Project Overview Video](https://www.youtube.com/watch?v=TWZiudul_ws&ab_channel=AliHadizadeh)

## Steps to Simulate in Modelsim

1) Run `do compile.do` to compile the `.v` files into ModelSim.
2) Run `do simulate.do data.mid.mem` to copy the program in `data.mid.mem` to the memory
3) Run `do wave.do` to simulate some waveforms.
4) Run `run 10000ns` to run the processor for some time.
