#encode"U"
def encodeU(inst_name,ops,line_no):
    info=instructions[inst_name]

    if len(ops)!=2:
        raise Exception("line"+str(line_no)+":wrong operand count")

    rd_name=ops[0].strip()
    imm_text=ops[1].strip()

    if rd_name not in registers:
        raise Exception("line"+str(line_no)+":invalid register")

    rd=registers[rd_name]

    try:
        imm=int(imm_text,0)
    except:
        raise Exception("line"+str(line_no)+":invalid immediate")

    if not check_range(imm,32):
        raise Exception("line"+str(line_no)+":immediate out of range")

    imm_bits=toBinary(imm,32)[:20]

    return imm_bits+rd+info["opcode"]
