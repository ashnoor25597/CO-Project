def encodeS(instruction):

    try:

        op, rest= instruction.split(" ", 1)

        if op not in instructions:
            return "Error: invalid instruction"
        
        if "func3" not in instructions[op]:
            return "Error: Invalid S-type instruction"
        
        parts= rest.split(",")
        if len(parts)!=2:
            return "Error: Invalid instruction format"
        
        rs2, address=parts
        rs2=rs2.strip()
        address=address.strip()

        if rs2 not in registers:
            return "Error: Invalid rs2 register"
        
        if "(" not in address or ")" not in address:
            return "Error: Invalid memory format"

        

        imm= address.split("(")[0].strip()

        rs1= address.split("(")[1].replace(")", "").strip()
        if rs1 not in registers:
            return "Error: Invalid rs1 register"


        rs1_binary= registers[rs1]
        rs2_binary= registers[rs2]

        if not check_num_val(imm):
            return "Error: Invalid immediate value"

        imm_int=convert_int(imm)

        if not check_range(imm_int):
            return "Error: Immediate out of range"

        imm_bin= toBinary(imm_int,12)
        upper=imm_bin[:7]
        lower=imm_bin[7:]

        return upper + rs2_binary + rs1_binary +instructions[op]["func3"] +lower + instructions[op]["opcode"]
    
    except ValueError:
        return "Error: Invalid instruction format"
    




