import sys, re # written by Balaji Venkatesh

DEPTH = 256
DUAL_REG_INSTR = {'LOAD': 0b0000, 'STORE': 0b0010, 'ADD': 0b0100, 'SUB':0b0110, 'NAND': 0b1000,
	'VLOAD': 0b1010, 'VADD': 0b1110, 'VSTORE': 0b1100}
BRANCH_INSTR = {'BZ':0b0101, 'BNZ':0b1001, 'BPZ':0b1101}
NAMESPACE = ['LOAD','STORE','ADD','SUB','VLOAD','VADD','VSTORE','NAND','BZ','BNZ','BPZ','ORI',
	'SHIFT','SHIFTL','SHIFTR','STOP','NOP','K0','K1','K2','K3','V0','V1','V2','V3','DB','ORG']

def assembler(inFilename, outFilename, memFilename): # main assembler

	try: # read input file
		with open(inFilename, 'r') as inF: assembly = inF.read()
	except OSError as err: error(err)
	# upper, split row and col, remove commas/parantheses/comments
	assembly = [line.partition(';')[0].strip().split() for line in re.sub(':|,|\(|\)',' ', assembly).upper().splitlines()]
	
	preproc = [] # preprocessed stuff
	labels = {} # label list
	for lineNum, line in enumerate(assembly): # read labels
		firstPass(line, labels, preproc, lineNum) # lineNum is used for error reporting
	preproc = [([labels.get(arg, arg) for arg in line[0]],line[1]) for line in preproc]
	binary = [0]*DEPTH # binary output
	address = 0
	for line, lineNum in preproc: # encode! (third pass)
		try:
			if address > DEPTH: error('Not enough memory for this many instructions', lineNum)
			elif line[0] in DUAL_REG_INSTR:
				binary[address] = register(line[1]) << 6 | register(line[2]) << 4 |	DUAL_REG_INSTR[line[0]]
			elif line[0] in BRANCH_INSTR:
				binary[address] = immediate(4,line[1]-address-1) << 4 | BRANCH_INSTR[line[0]]
			elif line[0] == "ORI":
				binary[address] = immediate(5,line[1]) << 3 | 0b111
			elif line[0] == "SHIFT":
				binary[address] = register(line[1]) << 6 | immediate(3,line[2]) << 3 | 0b011
			elif line[0] == "SHIFTL":
				binary[address] = register(line[1]) << 6 | immediate(2,line[2]) << 3 | 0b100011
			elif line[0] == "SHIFTR":
				binary[address] = register(line[1]) << 6 | immediate(2,line[2]) << 3 | 0b000011
			elif line[0] == "STOP":	binary[address] = 0b00000001
			elif line[0] == "NOP": binary[address] = 0b10000001
			elif line[0] == "DB": binary[address] = immediate(8, line[1])
			elif line[0] == "ORG": address = immediate(8, line[1])-1
			else: raise ValueError(f'Invalid instruction "{line[0]}"')
			address += 1
		except Exception as err: error(err, lineNum)

	out = f'DEPTH = {DEPTH};\nWIDTH = 8;\nADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\nCONTENT\nBEGIN\n'
	mem = '// memory data file (do not edit the following line - required for mem load use'\
		+'\n// instance=/multicycle/DataMem/b2v_inst/altsyncram_component/mem_data'\
		+'\n// format=mti addressradix=h dataradix=h version=1.0 wordsperline=1'
	for i in range(256):
		out += f'\n{i:02x} : {binary[i]:02x};'.upper()
		mem += f'\n{i:02x}: {binary[i]:02x}'.lower()
	out += '\n\nEND;\n'
	mem += '\n'
	try:
		with open(outFilename, 'w') as outF: outF.write(out)
		with open(memFilename, 'w') as memF: memF.write(mem)
	except OSError as err: error(err)

	print(f'Success!\n\nCompiled {inFilename} to {outFilename} and {memFilename}\n')

def firstPass(line, labels, preproc, lineNum): # read labels, rem empty lines
	if len(line) == 0: return
	if line[0] in NAMESPACE: preproc.append((line,lineNum))
	else: # we found a label!
		if line[0] in labels: error(f'Label "{line[0]}" already exists', lineNum)
		labels[line[0]] = len(preproc)
		firstPass(line[1:], labels, preproc, lineNum) # continue on the remaining line

def register(k): # register parser
	try: return {"K0":0b00,"K1":0b01,"K2":0b10,"K3":0b11,"V0":0b00,"V1":0b01,"V2":0b10,"V3":0b11}[k]
	except KeyError: raise ValueError(f'Invalid register "{k}"') from None

def immediate(n, imm): # immediate parser: IMMn(j)
	try: # deal with bases
		imm = str(imm)
		if imm.startswith('0B'): i = int(imm.removeprefix('0B'),2)
		elif imm.startswith('0X'): i = int(imm.removeprefix('0X'),16)
		elif imm.startswith('0'): i = int(imm,8)
		else: i = int(imm)
	except ValueError: raise ValueError(f'Invalid immediate "{imm}"') from None
	if n == 3 and i > 0: i = i | 0b100 # IMM3: one's complement
	elif n == 3 and i < 0: i = i & 0b011
	elif i < 0: i += 2 ** n # two's complement
	if(i.bit_length() > n or i < 0): raise ValueError(f'"{imm}" cannot be represented as IMM{n}') 
	return i

def error(err, lineNum = None): # error reporter
	print(f'\n[Error, line {lineNum+1}] {err}\n' if lineNum else f'\n[Error] {err}\n')
	sys.exit()

if __name__ == '__main__': # commandline argument logic block
	if (len(sys.argv) == 1 or sys.argv[1] == '-h'):
		print('\nusage: python compiler.py in [out] [mem]\nArguments:\nin:  input assembly file (required)'\
			+'\nout: output file 1 (default:"data.mid")\nmem: output file 2 (default: out+".mem")\n')
		sys.exit()
	out = sys.argv[2] if len(sys.argv)>=3 else 'data.mif'
	assembler(sys.argv[1], out, sys.argv[3] if len(sys.argv)>=4 else out+'.mem')