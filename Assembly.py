import sys

def read_file(filename):
    lines=[]
    
    with open(filename, "r") as file:
        for line in file:
            line=line.strip()
            if line=="":
                continue
            lines.append(line)
    
    return lines

registers={
"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100",
"t0":"00101","t1":"00110","t2":"00111",
"s0":"01000","fp":"01000","s1":"01001",
"a0":"01010","a1":"01011","a2":"01100","a3":"01101","a4":"01110","a5":"01111","a6":"10000","a7":"10001",
"s2":"10010","s3":"10011","s4":"10100","s5":"10101","s6":"10110","s7":"10111","s8":"11000","s9":"11001","s10":"11010","s11":"11011",
"t3":"11100","t4":"11101","t5":"11110","t6":"11111"
}

instructions={
"add":{"type":"R","opcode":"0110011","func3":"000","func7":"0000000"},
"sub":{"type":"R","opcode":"0110011","func3":"000","func7":"0100000"},
"sll":{"type":"R","opcode":"0110011","func3":"001","func7":"0000000"},
"slt":{"type":"R","opcode":"0110011","func3":"010","func7":"0000000"},
"sltu":{"type":"R","opcode":"0110011","func3":"011","func7":"0000000"},
"xor":{"type":"R","opcode":"0110011","func3":"100","func7":"0000000"},
"srl":{"type":"R","opcode":"0110011","func3":"101","func7":"0000000"},
"or":{"type":"R","opcode":"0110011","func3":"110","func7":"0000000"},
"and":{"type":"R","opcode":"0110011","func3":"111","func7":"0000000"},
"lw":{"type":"I","opcode":"0000011","func3":"010"},
"addi":{"type":"I","opcode":"0010011","func3":"000"},
"sltiu":{"type":"I","opcode":"0010011","func3":"011"},
"jalr":{"type":"I","opcode":"1100111","func3":"000"},
"sw":{"type":"S","opcode":"0100011","func3":"010"},
"beq":{"type":"B","opcode":"1100011","func3":"000"},
"bne":{"type":"B","opcode":"1100011","func3":"001"},
"blt":{"type":"B","opcode":"1100011","func3":"100"},
"bge":{"type":"B","opcode":"1100011","func3":"101"},
"bltu":{"type":"B","opcode":"1100011","func3":"110"},
"bgeu":{"type":"B","opcode":"1100011","func3":"111"},
"lui":{"type":"U","opcode":"0110111"},
"auipc":{"type":"U","opcode":"0010111"},
"jal":{"type":"J","opcode":"1101111"}
}

def toBinary(value,bits):
    num=int(value)
    if num<0:
        num=(1<<bits)+num
    binary=bin(num)[2:]
    return binary.zfill(bits)

def check_range(value, bits):
    minimum=-(2**(bits-1))
    maximum=(2**(bits-1))-1

    if minimum<=value<=maximum:
        return True
    else:
        return False
    
def check_num_val(num):
    
    if len(num)==0:
        return False
    
    if num[0]=="-":
        num=num[1:]

    if num.startswith ("0x") or num.startswith("0X"):
        hex=num[2:]

        if len(hex)==0:
            return False
        
        for char in hex:
            if not(char.isdigit() or char.lower() in "abcdef"):
                return False
        
        return True
    

    for char in num:
        if not char.isdigit():
            return False
        
    return True

def convert_int(num):
    
    
    if num.startswith("0x") or num.startswith("0X") or num.startswith("-0x") or num.startswith("-0X"):
        return int(num, 16)    
    
    if num.startswith("-"):
        return int(num)
    
    return int(num)

def check_label(my_label):

    if len(my_label)==0:
        return "Label is empty"
    
    if not my_label[0].isalpha():
        return "Invalid Label"
    
    for char in my_label:
        if not (char.isalnum() or char =="_"):
            return "Invalid Label"
        
    return True

def pass1(assembly_code):
    symbol_table={}
    pc=0
    for line in assembly_code:
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            label=line.split(':',1)[0].strip()
            check=check_label(label)
            if check!=True:
                print("Error: ", check)
                return{}
            if label in symbol_table:
                print("Error: Duplicate label", label)
                return {}
            symbol_table[label]=pc
            parts=line.split(':',1)[1].strip()
            if parts:
                pc+=4
        else:
            pc+=4
    return symbol_table

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


def encodeB(instruction,reg1,reg2,branch_offset):
    try:
        if instruction not in instructions:
            raise ValueError("Invalid instruction")
        instr_info=instructions[instruction]
        if instr_info["type"]!="B":
            raise ValueError("Instruction is not B-type")
        if reg1 not in registers or reg2 not in registers:
            raise ValueError("Invalid register name")
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
    except Exception as e:
        return "Error in encodeB:" +str(e)
        



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
        return imm_bits+rs1+info["func3"]+rd+info["opcode"]

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
        return imm_bits+rs1+info["func3"]+rd+info["opcode"]


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
        return"Error in encodeR:" +str(e)
        


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

    if not check_range(imm,20):
        raise Exception("line"+str(line_no)+":immediate out of range")

    imm_bits=toBinary(imm,20)[:20]

    return imm_bits+rd+info["opcode"]

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

        if not check_range(imm_int,21):
            return "Error: Immediate out of range"
        imm_bin= toBinary(imm_int,21)

        imm_20=imm_bin[0]
        imm10_1=imm_bin[10:20]
        imm11=imm_bin[9]
        imm19_12=imm_bin[1:9]

        return imm_20 + imm10_1 + imm11 +imm19_12 +rd_binary + instructions[op]["opcode"]
    
    except ValueError:
        return "Error: Invalid instruction format"
    
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

        if not check_range(imm_int,12):
            return "Error: Immediate out of range"

        imm_bin= toBinary(imm_int,12)
        upper=imm_bin[:7]
        lower=imm_bin[7:]

        return upper + rs2_binary + rs1_binary +instructions[op]["func3"] +lower + instructions[op]["opcode"]
    
    except ValueError:
        return "Error: Invalid instruction format"

def parse_instr(line):
    line=line.strip()

    if " " in line:
        op, rest=line.split(" ", 1)
    else:
        op=line
        rest=""
    


    if op in instructions:
        inst_type=instructions[op]["type"]

        if inst_type=="R":

            rd ,rs1, rs2= rest.split(",")
            rd= rd.strip()
            rs1=rs1.strip()
            rs2=rs2.strip()
            binary=encodeR(op,rd,rs1,rs2)

        elif inst_type=="I":

            ops=rest.split(",")
            binary=encodeI(op,ops,0)

        elif inst_type=="S":
            binary=encodeS(line)
        
        elif inst_type=="B":

            rs1, rs2, imm=rest.split(",")
            rs1=rs1.strip()
            rs2=rs2.strip()
            imm=int(imm.strip(),0)
            binary=encodeB(op,rs1,rs2,imm)

        elif inst_type=="U":
            ops=rest.split(",")
            binary=encodeU(op,ops,0)
            

        elif inst_type=="J":
            binary=encodeJ(line)
        
        return binary

    else:
        return "Error: Instruction not found"
    
def output(binary_txt):
    
    output_lines=[]

    output_lines.append(binary_txt)

    with open(sys.argv[2], "w") as f:
        for line in output_lines:
            f.write(line+"\n")


def main():

    #reading assembly file
    assembly_code=read_file(sys.argv[1])

    #check virtual halt

    halt_check=check_virtual_halt(assembly_code)

    if halt_check!=True:
        print(halt_check)
        return 
    
    #PASS1
    symbol_table=pass1(assembly_code)

    binary_output=[]
    line_no=1

    #PASS2
    for line in assembly_code:

        line=line.strip()

        if line == "" or line.startswith("#"):
            continue

        if ":" in line:
            parts= line.split(":", 1)
            line=parts[1].strip()

            if line=="":
                continue

        binary=parse_instr(line)

        binary_output.append(binary)

        line_no+=1


    with open(sys.argv[2], "w")as f:

        for b in binary_output:
            f.write(b+"\n")

if __name__=="__main__":
    main()


       

