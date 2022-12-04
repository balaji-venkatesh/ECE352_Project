onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /multicycle_tb/reset
add wave -noupdate /multicycle_tb/clock
add wave -noupdate /multicycle_tb/DUT/Control/instr
add wave -noupdate /multicycle_tb/DUT/Control/snot
add wave -noupdate -radix unsigned /multicycle_tb/DUT/Control/state
add wave -noupdate -divider {Standard Registers}
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/reg0
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/reg1
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/reg2
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/reg3
add wave -noupdate -divider {Vector Registers}
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/VRF_block/k0
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/VRF_block/k1
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/VRF_block/k2
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/VRF_block/k3
add wave -noupdate -divider {Other}
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/R2wire
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/VRegWire
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/MEMwire
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/T0Ld
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/T1Ld
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/T2Ld
add wave -noupdate -radix hexadecimal /multicycle_tb/DUT/T3Ld

TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {2500 ns} 0}
configure wave -namecolwidth 227
configure wave -valuecolwidth 57
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1000
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ns
update
WaveRestoreZoom {0 ps} {1000 ns}