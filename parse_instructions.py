def parse_instr(line):
    line=line.strip()
    parts=line.split()
    
    op=parts[0]

    if op in instructions:
        inst_type=instructions[op]["type"]

        if inst_type=="R":
            binary=encodeR(line)

        elif inst_type=="I":
            binary=encodeI(line)

        elif inst_type=="S":
            binary=encodeS(line)
        
        elif inst_type=="B":
            binary=encodeB(line)

        elif inst_type=="U":
            binary=encodeU(line)

        elif inst_type=="J":
            binary=encodeJ(line)
        
        return binary

    else:
        return "Error: Instruction not found"
    
   

    
