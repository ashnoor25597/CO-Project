def encodeB(instruction,reg1,reg2,branch_offset):
    instr_info=instructions[instruction]
    opcode=instr_info["opcode"]
    func3=instr_info["func3"]
    rs1=registers[reg1]
    rs2=registers[reg2]
    if branch_offset<0:
        branch_offset=(1<<13)+branch_offset
    imm=format(branch_offset,'013b')
    imm12=imm[0]
    imm10_5=imm[1:7]
    imm4_1=imm[7:11]
    imm11=imm[11]
    encode=imm12+imm10_5+rs2+rs1+func3+imm4_1+imm11+opcode
    return encode
