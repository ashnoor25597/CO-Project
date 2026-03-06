def encodeR(instruction,dest_reg,src1_reg,src2_reg):
    instr_info=instructions[instruction]
    opcode=instr_info["opcode"]
    func3=instr_info["func3"]
    func7=instr_info["func7"]
    rd=registers[dest_reg]
    rs1=registers[src1_reg]
    rs2=registers[src2_reg]
    encode=func7+rs2+rs1+func3+rd+opcode
    return encode
