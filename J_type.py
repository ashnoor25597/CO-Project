def encodeJ(instr):
    try:

        op, rest= instr.split(" ", 1)

        if op not in instructions:
            return "Error: Invalid instruction"

        rd,imm= rest.split(",")

        rd=rd.strip()
        imm=imm.strip()

        if rd not in registers:
            return "Error: Invalid register"

        rd_binary=registers[rd]

        if not check_num_val(imm):
            return "Error: Invalid immediate value"

        imm_int=convert_int(imm)

        if not check_range(imm_int):
            return "Error: Immediate out of range"
        imm_bin= toBinary(imm_int,21)

        imm_20=imm_bin[0]
        imm10_1=imm_bin[10:20]
        imm11=imm_bin[9]
        imm19_12=imm_bin[1:9]

        return imm_20 + imm10_1 + imm11 +imm19_12 +rd_binary + instructions[op]["opcode"]
    
    except ValueError:
        return "Error: Invalid instruction format"



