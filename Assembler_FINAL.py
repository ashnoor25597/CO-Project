import sys

def read_file(filename=None):
    lines=[]

    if filename:   # if a filename is provided
        with open(filename,"r") as file:
            for line in file:
                line=line.strip()
                if line=="":
                    continue
                lines.append(line)
    else:          # read from stdin (used by tester)
        for line in sys.stdin:
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

symbol_table={}
pc=0
line_no=0

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
    for i, line in enumerate(assembly_code,1):
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            label=line.split(':',1)[0].strip()
            check=check_label(label)
            if check!=True:
                print(f"Error in line {i}: {check}")
                return{}
            if label in symbol_table:
                print(f"Error in line {i}: Duplicate label {label}")
                return {}
            symbol_table[label]=pc
            parts=line.split(':',1)[1].strip()
            if parts:
                pc+=4
        else:
            pc+=4
    return symbol_table

def check_virtual_halt(assembly_code):

    for line in assembly_code:

        line=line.strip()

        if line=="" or line.startswith("#"):
            continue

        if ":" in line:
            line=line.split(":",1)[1].strip()

        if line=="":
            continue

        line=line.replace(","," ")
        parts=line.split()

        if len(parts)>=4 and parts[0]=="beq" and parts[1]=="zero" and parts[2]=="zero" and parts[3]=="0":
            return True

    return "Error: Missing virtual halt"
def encodeB(instruction, rs1_name, rs2_name, branch_offset):

    info = instructions[instruction]

    opcode = int(info["opcode"],2)
    funct3 = int(info["func3"],2)

    rs1 = int(registers[rs1_name],2)
    rs2 = int(registers[rs2_name],2)

    imm = branch_offset

    imm12 = (imm >> 12) & 1
    imm11 = (imm >> 11) & 1
    imm10_5 = (imm >> 5) & 0x3F
    imm4_1 = (imm >> 1) & 0xF

    inst = (
        (imm12 << 31) |
        (imm10_5 << 25) |
        (rs2 << 20) |
        (rs1 << 15) |
        (funct3 << 12) |
        (imm4_1 << 8) |
        (imm11 << 7) |
        opcode
    )

    return format(inst, "032b")
   
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
        return f"Error in line {line_no}: {str(e)}"
        


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
    imm_bits=toBinary(imm,20)
    return imm_bits+rd+info["opcode"]


def encodeJ(instr):
    try:
        op,rest=instr.split(" ",1)
        if op not in instructions:
            return f"Error in line {line_no}: Invalid instruction"
        rd,imm=rest.split(",")
        rd=rd.strip()
        imm=imm.strip()
        if rd not in registers:
            return f"Error in line {line_no}: Invalid register"
        rd_binary=registers[rd]
        if not check_num_val(imm):
            return f"Error in line {line_no}: Invalid immediate value"
        imm_int=convert_int(imm)
        if not check_range(imm_int,21):
            return f"Error in line {line_no}: Immediate out of range"
        imm_bin=toBinary(imm_int,21)
        imm_20=imm_bin[0]
        imm10_1=imm_bin[10:20]
        imm11=imm_bin[9]
        imm19_12=imm_bin[1:9]
        return imm_20+imm10_1+imm11+imm19_12+rd_binary+instructions[op]["opcode"]
    except ValueError:
        return f"Error in line {line_no}: Invalid instruction format"


def encodeS(instruction):
    try:
        op,rest=instruction.split(" ",1)
        if op not in instructions:
            return f"Error in line {line_no}: invalid instruction"
        if "func3" not in instructions[op]:
            return f"Error in line {line_no}: Invalid S-type instruction"
        parts=rest.split(",")
        if len(parts)!=2:
            return f"Error in line {line_no}: Invalid instruction format"
        rs2,address=parts
        rs2=rs2.strip()
        address=address.strip()
        if rs2 not in registers:
            return f"Error in line {line_no}: Invalid rs2 register"
        if "(" not in address or ")" not in address:
            return f"Error in line {line_no}: Invalid memory format"
        imm=address.split("(")[0].strip()
        rs1=address.split("(")[1].replace(")","").strip()
        if rs1 not in registers:
            return f"Error in line {line_no}: Invalid rs1 register"
        rs1_binary=registers[rs1]
        rs2_binary=registers[rs2]
        if not check_num_val(imm):
            return f"Error in line {line_no}: Invalid immediate value"
        imm_int=convert_int(imm)
        if not check_range(imm_int,12):
            return f"Error in line {line_no}: Immediate out of range"
        imm_bin=toBinary(imm_int,12)
        upper=imm_bin[:7]
        lower=imm_bin[7:]
        return upper+rs2_binary+rs1_binary+instructions[op]["func3"]+lower+instructions[op]["opcode"]
    except ValueError:
        return f"Error in line {line_no}: Invalid instruction format"


def parse_instr(line,line_no):
    global pc,symbol_table
    line=line.strip()
    line=line.replace("\t"," ").strip()
    parts=line.split(maxsplit=1)
    op=parts[0].strip()
    if len(parts)>1:
        rest=parts[1]
    else:
        rest=""
    if op in instructions:
        inst_type=instructions[op]["type"]
        if inst_type=="R":
            parts=rest.split(",")
            if len(parts)!=3:
                return f"Error in line {line_no}: Invalid operand count"
            rd,rs1,rs2=parts
            rd=rd.strip()
            rs1=rs1.strip()
            rs2=rs2.strip()
            binary=encodeR(op,rd,rs1,rs2)
        elif inst_type=="I":
            try:
                ops=rest.split(",")
                binary=encodeI(op,ops,line_no)
            except Exception as e:
                return f"Error in line {line_no}: {str(e)}"
        elif inst_type=="S":
            binary=encodeS(line)
        elif inst_type=="B":
            parts=rest.split(",")
            if len(parts)!=3:
                return f"Error in line {line_no}: Invalid operand count"
            rs1,rs2,imm=[x.strip() for x in parts]
            if rs1 not in registers or rs2 not in registers:
                return f"Error in line {line_no}: Invalid register"
            if imm in symbol_table:
                target=symbol_table[imm]
                imm=target-pc
            elif check_num_val(imm):
                imm=convert_int(imm)
            else:
                return f"Error in line {line_no}: Invalid label or immediate"
            if not check_range(imm,13):
                return f"Error in line {line_no}: Immediate out of range"
            binary=encodeB(op,rs1,rs2,imm)
        elif inst_type=="U":
            ops=rest.split(",")
            binary=encodeU(op,ops,line_no)
        elif inst_type=="J":
            rd,imm=rest.split(",")
            rd=rd.strip()
            imm=imm.strip()
            if imm in symbol_table:
                imm=symbol_table[imm]-pc
            elif check_num_val(imm):
                imm=convert_int(imm)
            else:
                return f"Error in line {line_no}: Invalid label or immediate"
            new_line=op+" "+rd+","+str(imm)
            binary=encodeJ(new_line)
        return binary


def output(binary_txt):
    output_lines=[]
    output_lines.append(binary_txt)
    with open(sys.argv[2],"w") as f:
        for line in output_lines:
            f.write(line+"\n")


def main():
    global pc
    pc=0
    global symbol_table
    if len(sys.argv)>1:
        assembly_code=read_file(sys.argv[1])
    else:
        assembly_code=read_file()
    halt_check=check_virtual_halt(assembly_code)
    if halt_check!=True:
        print(halt_check)
        if len(sys.argv)>2:
            open(sys.argv[2],"w").close()
        return
    symbol_table=pass1(assembly_code)
    binary_output=[]
    global line_no
    line_no=1
    for line in assembly_code:
        line=line.strip()
        if line=="" or line.startswith("#"):
            continue
        if ":" in line:
            parts=line.split(":",1)
            line=parts[1].strip()
            if line=="":
                continue
        binary=parse_instr(line,line_no)
        if isinstance(binary,str) and binary.startswith("Error"):
            print(binary)
            if len(sys.argv)>2:
                open(sys.argv[2],"w").close()
            return
        binary_output.append(binary)
        pc+=4
        line_no+=1
    if len(sys.argv)>2:
        with open(sys.argv[2],"w") as f:
            for b in binary_output:
                f.write(b+"\n")
    else:
        for b in binary_output:
            print(b)

if __name__=="__main__":
    main()
