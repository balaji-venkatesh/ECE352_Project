ori		0b10100
shiftl  K1 2
vload	V0	K1
vadd	V1	V0
vadd	V1	V0
vstore 	V1	K1
vload	V2	K1
stop

org	0x50
db	0x25
db	0x12
db  0x23
db	0x27