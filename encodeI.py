def encodeI(inst_name,ops,line_no):
    info=instructions[inst_name]
    if inst_name=="lw":
        if len(ops)!=2:
            raise Exception("line"+str(line_no)+":wrong operand count")
        rd_name=ops[0].strip()
        mem_op=ops[1].strip()
        rd=reg_bits(rd_name,line_no)
        if "(" not in mem_op or ")" not in mem_op:
            raise Exception("line"+str(line_no)+":invalid memory format")
        left=mem_op[:mem_op.index("(")].strip()
        inside=mem_op[mem_op.index("(")+1:mem_op.index(")")].strip()

        try:
            imm=int(left,0)
        except:
            raise Exception("line"+str(line_no)+":invalid immediate")
        rs1=reg_bits(inside,line_no)
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
        rd=reg_bits(rd_name,line_no)
        rs1=reg_bits(rs1_name,line_no)

        try:
            imm=int(imm_text,0)
        except:
            raise Exception("line"+str(line_no)+":invalid immediate")

        if not check_range(imm,12):
            raise Exception("line"+str(line_no)+":immediate out of range")
        imm_bits=toBinary(imm,12)
        return imm_bits+rs1+info["funct3"]+rd+info["opcode"]
