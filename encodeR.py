def encodeR(instruction,dest_reg,src1_reg,src2_reg):
    try:
        if instruction not in instructions:
            raise ValueError("Invalid instruction")
        instr_info=instructions[instruction]
        if instr_info["type"]!="R":
            raise ValueError("Instruction is not R-type")
        if dest_reg not in registers or src1_reg not in registers or src2_reg not in registers:
            raise ValueError("Invalid register name")
        opcode=instr_info["opcode"]
        func3=instr_info["func3"]
        func7=instr_info["func7"]
        rd=registers[dest_reg]
        rs1=registers[src1_reg]
        rs2=registers[src2_reg]
        encode=func7+rs2+rs1+func3+rd+opcode
        return encode
    except Exception as e:
        print("Error in encodeR:",e)
        return None
