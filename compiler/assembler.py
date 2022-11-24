import sys, re

# assembly parameters
DEPTH = 256

# constants
DUAL_REG_INSTR = {'LOAD': 0b0000, 'STORE': 0b0010, 
	'ADD': 0b0100, 'SUB':0b0110, 'NAND': 0b1000,
	'VLOAD': 0b1010, 'VADD': 0b1110, 'VSTORE': 0b1100}
BRANCH_INSTR = {'BZ':0b0101, 'BNZ':0b1001, 'BPZ':0b1101}
NAMESPACE = ['LOAD','STORE','ADD','SUB','VLOAD','VADD','VSTORE','NAND',
	'BZ','BNZ','BPZ','ORI','SHIFT','SHIFTL','SHIFTR','STOP','NOP',
	'K1','K2','K3','K4','X1','X2','X3','X4','DB','ORG']

##### main assembler #####

# avengers
def assemble(inFilename, outFilename, memFilename): 

	try: # read input file
		with open(inFilename, 'r') as inF: asm = inF.read()
	except OSError as err: error(err)
	# upper, split row and col, remove commas/parantheses/comments
	asm = [line.partition(';')[0].strip().split() for line in 
		re.sub(',|\(|\)',' ', asm).upper().splitlines()]
	
	pre = [] # preprocessed stuff
	lbls = {} # label list
	
	for liNo, line in enumerate(asm): # read labels
		try: 
			readLbls(line, lbls, pre, liNo) # liNo is used for error reporting
			if len(pre) > DEPTH: error('Not enough memory for this many instructions', liNo)
		except Exception as err: error(err, liNo)
	# replace labels
	pre = [([lbls.get(arg, arg) for arg in line[0]],line[1]) for line in pre]

	bny = [0]*DEPTH # binary output
	address = 0

	for (line, liNo) in pre: 
		try:
			if line[0] in DUAL_REG_INSTR:
				bny[address] = (reg(line[1]) << 6 | reg(line[2]) << 4 | DUAL_REG_INSTR[line[0]])
			elif line[0] in BRANCH_INSTR:
				bny[address] = (imm(4, line[1]) << 4 | BRANCH_INSTR[line[0]])
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

	out = f'DEPTH = {DEPTH};\nWIDTH = 8;\nADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\nCONTENT\nBEGIN\n'
	mem = '// memory data file (do not edit the following line - required for mem load use'\
		+'\n// instance=/multicycle/DataMem/b2v_inst/altsyncram_component/mem_data'\
		+'\n// format=mti addressradix=h dataradix=h version=1.0 wordsperline=1'
	for i in range(256):
		out += f'\n{i:02x} : {bny[i]:02x};'.upper()
		mem += f'\n{i:02x}: {bny[i]:02x}'.lower()
	out += '\n\nEND;\n'
	mem += '\n'
	try:
		with open(outFilename, 'w') as outF: outF.write(out)
		with open(memFilename, 'w') as memF: memF.write(mem)
	except OSError as err: error(err)

	print(f'Success! Compiled {inFilename} to {outFilename} and {memFilename}\n')

##### helper functions #####

def readLbls(line, lbls, pre, liNo): # label reader, also removes empty lines, and assigns liNos
	if len(line) == 0: return
	if line[0] in NAMESPACE: pre.append((line,liNo))
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
	except ValueError: raise ValueError(f'Invalid immediate "{imm}"') from None
	if   n == 3 and i > 0: i = i | 0b100 # IMM3: one's complement
	elif n == 3 and i < 0: i = i & 0b011
	elif i < 0: 		   i += 2 ** n # two's complement
	if(i.bit_length() > n or i < 0): # check for IMM fit
		raise ValueError(f'"{imm}" cannot be represented as IMM{n}') 
	return i

def error(error, liNo = None): # error reporter
	if liNo : print(f'\n[Error, line {liNo+1}] {error}\n"Use -h for help.\n"')
	else: print(f'\n[Error] {error}\n"Use -h for help.\n')
	sys.exit()

if __name__ == '__main__': # commandline argument logic block
	numArgs = len(sys.argv)
	if (numArgs == 1):
		error('No input file provided')
	elif (sys.argv[1] == '-h'):
		print('usage: python compiler.py in [out] [outMem]\nArguments:')
		print('in\t: Assembly file (required)')
		print('out\t: Quartus memory file (default:"data.mid"}')
		print('outMem\t: ModelSim memory file (default: out+".mem"}')
		sys.exit()
	elif (numArgs == 2): assemble(sys.argv[1], 'data.mid',  'data.mid.mem')
	elif (numArgs == 3): assemble(sys.argv[1], sys.argv[2], sys.argv[2]+'.mem')
	elif (numArgs == 4): assemble(sys.argv[1], sys.argv[2], sys.argv[3])