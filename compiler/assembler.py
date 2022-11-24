import sys, re

DEPTH = 256

dualRegInstructions = {'LOAD': 0b0000, 'STORE':0b0010, 'ADD':0b0100, 'SUB':0b0110,
	'VLOAD':0b1010, 'VADD': 0b1110, 'VSTORE': 0b1100, 'NAND': 0b1000}
branchInstructions = {'BZ':0b0101, 'BNZ':0b1001, 'BPZ':0b1101}
namespace = ['LOAD', 'STORE', 'ADD', 'SUB', 'VLOAD', 'VADD', 'VSTORE', 'NAND', 
	'BZ', 'BNZ', 'BPZ', 'ORI', 'SHIFT', 'SHIFTL', 'SHIFTR', 'STOP', 'NOP', 
	'K1', 'K2', 'K3', 'K4', 'X1', 'X2', 'X3', 'X4', 'DB', 'ORG']

# the actual compiler goes here I guess
def assemble(inFilename, outFilename, memFilename): 

	try: # read input file
		with open(inFilename, 'r') as inF: asm = inF.read()
	except FileNotFoundError: error("Input file not found")
	# capitalise, split into lines and arguments, and remove commas, parantheses, and comments
	asm = [line.partition(';')[0].strip().split() for line in re.sub(',|\(|\)',' ', asm).upper().splitlines()]
	
	pre = [] # preprocessed stuff
	lbls = {} # label list
	
	# read labels
	for liNo, line in enumerate(asm):
		try: 
			readLbls(line, lbls, pre, liNo)
			if len(pre) > DEPTH: error('Not enough memory for this many instructions', liNo)
		except Exception as err: error(err, liNo)
	# replace labels
	pre = [([lbls.get(arg, arg) for arg in line[0]],line[1]) for line in pre]

	#print('\n'.join([str(l) for l in asm]))
	#print(lbls)
	#print('\n'.join([str(l) for l in pre]))

	bny = [0]*DEPTH # binary output
	address = 0

	for (line, liNo) in pre: 
		try:
			if line[0] in dualRegInstructions:
				bny[address] = (reg(line[1]) << 6 | reg(line[2]) << 4 | dualRegInstructions[line[0]])
			elif line[0] in branchInstructions:
				bny[address] = (imm(4, line[1]) << 4 | branchInstructions[line[0]])
			elif line[0] == "ORI":
				bny[address] = (imm(5,line[1]) << 3 | 0b111)
			elif line[0] == "SHIFT":
				bny[address] = (reg(line[1]) << 6 | imm(3,line[2]) << 3 | 0b011)
			elif line[0] == "SHIFTL":
				bny[address] = (reg(line[1]) << 6 | imm(2,line[2]) << 3 | 0b100011)
			elif line[0] == "SHIFTR":
				bny[address] = (reg(line[1]) << 6 | imm(2,line[2]) << 3 | 0b000011)
			elif line[0] == "STOP":	
				bny[address] = (0b00000001)
			elif line[0] == "NOP": 
				bny[address] = (0b10000001)
			elif line[0] == "DB":
				bny[address] = imm(8, line[1])
			elif line[0] == "ORG": 
				address = imm(8, line[1])-1
			else: raise ValueError(f'Invalid instruction "{line[0]}"')
			address += 1
		except Exception as err: error(err, liNo)

	for i in range(256):
		print(f'{i}\t{bny[i]}')


def readLbls(line, lbls, pre, liNo): # label reader, also removes empty lines, and assigns liNos
	if len(line) == 0: return
	if line[0] in namespace: pre.append((line,liNo))
	else: # we found a label!
		if line[0] in lbls:	raise KeyError(f'Label {line[0]} already exists')
		else:
			lbls[line[0]] = str(len(pre))
			readLbls(line[1:], lbls, pre, liNo) # continue on the remaining line


def reg(k): # register parser
	try: return {"K0":0b00,"K1":0b01,"K2":0b10,"K3":0b11}[k]
	except KeyError: raise ValueError(f'Invalid register "{k}"') from None


def imm(n, imm): # immediate parser: IMMn(j)
	try: # deal with bases
		if   imm.startswith('0B'): i = int(imm.removeprefix('0B'),2)
		elif imm.startswith('0X'): i = int(imm.removeprefix('0X'),16)
		elif imm.startswith('0'):  i = int(imm,8)
		else: 					   i = int(imm)
	except ValueError:
		raise ValueError(f'Invalid immediate "{imm}"') from None
	if n == 3 and i > 0:   i = i | 0b100 # IMM3: one's complement
	elif n == 3 and i < 0: i = i & 0b011
	elif i < 0: 		   i += 2 ** n # two's complement
	if(i.bit_length() > n or i < 0): # check for IMM fit
		raise ValueError(f'"{imm}" cannot be represented as IMM{n}') 
	return i


def error(error, liNo = None): # error reporter
	if liNo : print(f'[Error, line {liNo+1}] {error}')
	else: print(f'[Error] {error}')
	print("Use -h for help.\n")
	sys.exit()


if __name__ == '__main__': # commandline argument logic block
	numArgs = len(sys.argv)
	if (numArgs == 1):
		error('No input file provided')
	elif (sys.argv[1] == '-h'):
		print('usage: python compiler.py in [out] [outMem]')
		print('Arguments:')
		print('in\t: Assembly file \t Required')
		print('out\t: Quartus memory file \t Default:"data.mid"')
		print('outMem\t: ModelSim memory file \t Default: out+".mem"')
		sys.exit()
	elif (numArgs == 2):
		assemble(sys.argv[1],'data.mid','data.mid.mem')
	elif (numArgs == 3):
		assemble(sys.argv[1], sys.argv[2], sys.argv[2]+'.mem')
	elif (numArgs == 4):
		assemble(sys.argv[1], sys.argv[2], sys.argv[3])