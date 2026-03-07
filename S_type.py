def encodeS(instruction):

    op, rest= instruction.split(" ", 1)
    rs2, address= rest.split(",")

    rs2=rs2.strip()

    imm= address.split("(")[0].strip()

    rs1= address.split("(")[1].replace(")", "").strip()

    rs1_binary= registers[rs1]
    rs2_binary= registers[rs2]

    if check_num_val(imm)==False:
        return "Invalid value of immediate"

    imm_int=convert_int(imm)

    imm_bin= toBinary(imm_int,12)
    upper=imm_bin[:7]
    lower=imm_bin[7:]

    return upper + rs2_binary + rs1_binary +instructions[op]["func3"] +lower + instructions[op]["opcode"]




