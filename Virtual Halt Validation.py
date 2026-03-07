def check_virtual_halt(assembly_code):
    real_instructions=[]

    for line in assembly_code:
        line=line.strip()
        if line=="" or line.startswith("#"):
            continue
        if ":" in line:
            parts=line.split(":",1)
            line=parts[1].strip()
        if line=="":
            continue
        real_instructions.append(line.replace(" ",""))
    if len(real_instructions)==0:
        return "Error: Missing virtual halt"

    halt1="beqzero,zero,0"
    halt2="beqzero,zero,0x00000000"
    halt_found=False

    for i in range(len(real_instructions)):
        if real_instructions[i]==halt1 or real_instructions[i]==halt2:
            halt_found=True
            if i!=len(real_instructions)-1:
                return "Error: Halt not last instruction"

    if not halt_found:
        return "Error: Missing virtual halt"
    return True
