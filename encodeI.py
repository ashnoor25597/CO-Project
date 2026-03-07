#encode"I"
def encodeI(inst_name,ops,line_no):
    info=instructions[inst_name]
    if inst_name=="lw":
        if len(ops)!=2:
            raise Exception("line"+str(line_no)+":wrong operand count")
        rd_name=ops[0].strip()
        mem_op=ops[1].strip()

        if rd_name not in registers:
            raise Exception("line"+str(line_no)+":invalid register")
        rd=registers[rd_name]

        if "(" not in mem_op or ")" not in mem_op:
            raise Exception("line"+str(line_no)+":invalid memory format")
        left=mem_op[:mem_op.index("(")].strip()
        inside=mem_op[mem_op.index("(")+1:mem_op.index(")")].strip()

        try:
            imm=int(left,0)
        except:
            raise Exception("line"+str(line_no)+":invalid immediate")

        if inside not in registers:
            raise Exception("line"+str(line_no)+":invalid register")
        rs1=registers[inside]

        if not check_range(imm,12):
            raise Exception("line"+str(line_no)+":immediate out of range")
        imm_bits=toBinary(imm,12)
        return imm_bits+rs1+info["funct3"]+rd+info["opcode"]

    else:
        if len(ops)!=3:
            raise Exception("line"+str(line_no)+":wrong operand count")
        rd_name=ops[0].strip()
        rs1_name=ops[1].strip()
        imm_text=ops[2].strip()

        if rd_name not in registers or rs1_name not in registers:
            raise Exception("line"+str(line_no)+":invalid register")

        rd=registers[rd_name]
        rs1=registers[rs1_name]

        try:
            imm=int(imm_text,0)
        except:
            raise Exception("line"+str(line_no)+":invalid immediate")

        if not check_range(imm,12):
            raise Exception("line"+str(line_no)+":immediate out of range")
        imm_bits=toBinary(imm,12)
        return imm_bits+rs1+info["funct3"]+rd+info["opcode"]
