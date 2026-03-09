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
"s2":"10010","s3":"10011","s4":"10100","s5":"10101","s6":"10110","s7":"10111","s8":"11000","s9":"11001","s10":"11010","s1１":"１１０１１",
"t3":"１１１００","t4":"１１１０１","t5":"１１１１０","t6":"１１１１１"
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

symboltable={}
pc=0
lineno=0

def toBinary(value,bits):
    num=int(value)
    if num<0:
        num=(1<<bits)+num
    binary=bin(num)[2:]
    return binary.zfill(bits)

def checkrange(value,bits):
    minimum=-(2**(bits-1))
    maximum=(2**(bits-1))-1

    if minimum<=value<=maximum:
        return True
    else:
        return False

def checknumval(num):
    
    if len(num)==0:
        return False
    
    if num[0]=="-":
        num=num[1:]

    if num.startswith ("0x") or num.startswith("0X"):
        hexpart=num[2:]

        if len(hexpart)==0:
            return False
        
        for char in hexpart:
            if not(char.isdigit() or char.lower() in "abcdef"):
                return False
        
        return True
    

    for char in num:
        if not char.isdigit():
            return False
        
    return True

def convertint(num):
    
    
    if num.startswith("0x") or num.startswith("0X") or num.startswith("-0x") or num.startswith("-0X"):
        return int(num,16)    
    
    if num.startswith("-"):
        return int(num)
    
    return int(num)

def checklabel(mylabel):

    if len(mylabel)==0:
        return "Label is empty"
    
    if not mylabel[0].isalpha():
        return "Invalid Label"
    
    for char in mylabel:
        if not (char.isalnum() or char =="_"):
            return "Invalid Label"
        
    return True

def pass1(assemblycode):
    symboltable={}
    pc=0
    for i,line in enumerate(assemblycode,1):
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            label=line.split(':',1)[0].strip()
            check=checklabel(label)
            if check!=True:
                print(f"Error in line {i}: {check}")
                return{}
            if label in symboltable:
                print(f"Error in line {i}: Duplicate label {label}")
                return {}
            symboltable[label]=pc
            parts=line.split(':',1)[1].strip()
            if parts:
                pc+=4
        else:
            pc+=4
    return symboltable

def checkvirtualhalt(assemblycode):

    for line in assemblycode:

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

def encodeB(instruction,rs1name,rs2name,branchoffset):

    info=instructions[instruction]

    opcode=int(info["opcode"],2)
    funct3=int(info["func3"],2)

    rs1=int(registers[rs1name],2)
    rs2=int(registers[rs2name],2)

    imm=branchoffset

    imm12=(imm>>12)&1
    imm11=(imm>>11)&1
    imm105=(imm>>5)&0x3F
    imm41=(imm>>1)&0xF

    inst=(
        (imm12<<31) |
        (imm105<<25) |
        (rs2<<20) |
        (rs1<<15) |
        (funct3<<12) |
        (imm41<<8) |
        (imm11<<7) |
        opcode
    )

    return format(inst,"032b")

#encode"I"
def encodeI(instname,ops,lineno):
    info=instructions[instname]
    if instname=="lw":
        if len(ops)!=2:
            raise Exception("line"+str(lineno)+":wrong operand count")
        rdname=ops[0].strip()
        memop=ops[1].strip()

        if rdname not in registers:
            raise Exception("line"+str(lineno)+":invalid register")
        rd=registers[rdname]

        if "(" not in memop or ")" not in memop:
            raise Exception("line"+str(lineno)+":invalid memory format")
        leftpart=memop[:memop.index("(")].strip()
        insidepart=memop[memop.index("(")+1:memop.index(")")].strip()

        try:
            imm=int(leftpart,0)
        except:
            raise Exception("line"+str(lineno)+":invalid immediate")

        if insidepart not in registers:
            raise Exception("line"+str(lineno)+":invalid register")
        rs1=registers[insidepart]

        if not checkrange(imm,12):
            raise Exception("line"+str(lineno)+":immediate out of range")
        immbits=toBinary(imm,12)
        return immbits+rs1+info["func3"]+rd+info["opcode"]

    else:
        if len(ops)!=3:
            raise Exception("line"+str(lineno)+":wrong operand count")
        rdname=ops[0].strip()
        rs1name=ops[1].strip()
        immtext=ops[2].strip()

        if rdname not in registers or rs1name not in registers:
            raise Exception("line"+str(lineno)+":invalid register")

        rd=registers[rdname]
        rs1=registers[rs1name]

        try:
            imm=int(immtext,0)
        except:
            raise Exception("line"+str(lineno)+":invalid immediate")

        if not checkrange(imm,12):
            raise Exception("line"+str(lineno)+":immediate out of range")
        immbits=toBinary(imm,12)
        return immbits+rs1+info["func3"]+rd+info["opcode"]

def encodeR(instruction,destreg,src1reg,src2reg):
    try:
        if instruction not in instructions:
            raise ValueError("Invalid instruction")
        instrinfo=instructions[instruction]
        if instrinfo["type"]!="R":
            raise ValueError("Instruction is not R-type")
        if destreg not in registers or src1reg not in registers or src2reg not in registers:
            raise ValueError("Invalid register name")
        opcode=instrinfo["opcode"]
        func3=instrinfo["func3"]
        func7=instrinfo["func7"]
        rd=registers[destreg]
        rs1=registers[src1reg]
        rs2=registers[src2reg]
        encode=func7+rs2+rs1+func3+rd+opcode
        return encode
    except Exception as e:
        return f"Error in line {lineno}: {str(e)}"  

#encode"U"
def encodeU(instname,ops,lineno):
    info=instructions[instname]

    if len(ops)!=2:
        raise Exception("line"+str(lineno)+":wrong operand count")

    rdname=ops[0].strip()
    immtext=ops[1].strip()

    if rdname not in registers:
        raise Exception("line"+str(lineno)+":invalid register")

    rd=registers[rdname]

    try:
        imm=int(immtext,0)
    except:
        raise Exception("line"+str(lineno)+":invalid immediate")

    if not checkrange(imm,20):
        raise Exception("line"+str(lineno)+":immediate out of range")

    immbits=toBinary(imm,20)

    return immbits+rd+info["opcode"] 

def encodeJ(instr):
    try:

        op,rest=instr.split(" ",1)

        if op not in instructions:
            return f"Error in line {lineno}: Invalid instruction"

        rd,imm=rest.split(",")

        rd=rd.strip()
        imm=imm.strip()

        if rd not in registers:
            return f"Error in line {lineno}: Invalid register"

        rdbinary=registers[rd]

        if not checknumval(imm):
            return f"Error in line {lineno}: Invalid immediate value"

        immint=convertint(imm)

        if not checkrange(immint,21):
            return f"Error in line {lineno}: Immediate out of range"
        immbin=toBinary(immint,21)

        imm20=immbin[0]
        imm101=immbin[10:20]
        imm11=immbin[9]
        imm1912=immbin[1:9]

        return imm20+imm101+imm11+imm1912+rdbinary+instructions[op]["opcode"]
    
    except ValueError:
        return f"Error in line {lineno}: Invalid instruction format"
    


def encodeS(instruction):

    try:

        op,rest=instruction.split(" ",1)

        if op not in instructions:
            return f"Error in line {lineno}: invalid instruction"
        
        if "func3" not in instructions[op]:
            return f"Error in line {lineno}: Invalid S-type instruction"
        
        parts=rest.split(",")
        if len(parts)!=2:
            return f"Error in line {lineno}: Invalid instruction format"
        
        rs2,address=parts
        rs2=rs2.strip()
        address=address.strip()

        if rs2 not in registers:
            return f"Error in line {lineno}: Invalid rs2 register"
        
        if "(" not in address or ")" not in address:
            return f"Error in line {lineno}: Invalid memory format"

        imm=address.split("(")[0].strip()

        rs1=address.split("(")[1].replace(")","").strip()
        if rs1 not in registers:
            return f"Error in line {lineno}: Invalid rs1 register"

        rs1binary=registers[rs1]
        rs2binary=registers[rs2]

        if not checknumval(imm):
            return f"Error in line {lineno}: Invalid immediate value"

        immint=convertint(imm)

        if not checkrange(immint,12):
            return f"Error in line {lineno}: Immediate out of range"

        immbin=toBinary(immint,12)
        upperpart=immbin[:7]
        lowerpart=immbin[7:]

        return upperpart+rs2binary+rs1binary+instructions[op]["func3"]+lowerpart+instructions[op]["opcode"]
    
    except ValueError:
        return f"Error in line {lineno}: Invalid instruction format"
    
def parseinstr(line,lineno):
    global pc,symboltable
    line=line.strip()
    parts=line.split()

    line=line.replace("\t"," ").strip()

    parts=line.split(maxsplit=1)

    op=parts[0].strip()

    if len(parts)>1:
        rest=parts[1]
    else:
        rest=""

    if op in instructions:
        insttype=instructions[op]["type"]

        if insttype=="R":
            parts=rest.split(",")

            if len(parts)!=3:
                return f"Error in line {lineno}: Invalid operand count"
            
            rd,rs1,rs2=parts
            rd=rd.strip()
            rs1=rs1.strip()
            rs2=rs2.strip()
            binary=encodeR(op,rd,rs1,rs2)

        elif insttype=="I":
            try:
                ops=rest.split(",")
                binary=encodeI(op,ops,lineno)
            except Exception as e:
                return f"Error in line {lineno}: {str(e)}"

        elif insttype=="S":
            binary=encodeS(line)
        
        elif insttype=="B":
            parts=rest.split(",")

            if len(parts)!=3:
                return f"Error in line {lineno}: Invalid operand count"
            
            rs1,rs2,imm=[x.strip() for x in parts]
            if rs1 not in registers or rs2 not in registers:
                return f"Error in line {lineno}: Invalid register"
            
            if imm in symboltable:
                target=symboltable[imm]
                imm=target-pc
            elif checknumval(imm):
                imm=convertint(imm)
            else:
                return f"Error in line {lineno}: Invalid label or immediate"
            
            if not checkrange(imm,13):
                return f"Error in line {lineno}: Immediate out of range"
                
            binary=encodeB(op,rs1,rs2,imm)

        elif insttype=="U":
            ops=rest.split(",")
            binary=encodeU(op,ops,lineno)

        elif insttype=="J":
            rd,imm=rest.split(",")
            rd=rd.strip()
            imm=imm.strip()

            if imm in symboltable:
                imm=symboltable[imm]-pc
            elif checknumval(imm):
                imm=convertint(imm)
            else:
                return f"Error in line {lineno}: Invalid label or immediate"
            
            newline=op+" "+rd+","+str(imm)
            binary=encodeJ(newline)
        return binary

def output(binarytxt):
    
    outputlines=[]

    outputlines.append(binarytxt)

    with open(sys.argv[2],"w") as f:
        for line in outputlines:
            f.write(line+"\n")

def main():
    global pc
    pc=0
    global symboltable

    #reading assembly file
    if len(sys.argv)>1:
        assemblycode=read_file(sys.argv[1])
    else:
        assemblycode=read_file()

    #assemblycode = [line.strip() for line in sys.stdin if line.strip() != ""]

    #check virtual halt
    haltcheck=checkvirtualhalt(assemblycode)

    if haltcheck!=True:
        print(haltcheck)
        
        if len(sys.argv)>2:
            open(sys.argv[2],"w").close()
        return
    
    #PASS1
    symboltable=pass1(assemblycode)

    binaryoutput=[]
    global lineno
    lineno=1

    #PASS2
    for line in assemblycode:

        line=line.strip()

        if line=="" or line.startswith("#"):
            continue

        if ":" in line:
            parts=line.split(":",1)
            line=parts[1].strip()

            if line=="":
                continue

        binary=parseinstr(line,lineno)

        if isinstance(binary,str) and binary.startswith("Error"):
            print(binary)
            
            if len(sys.argv)>2:
                open(sys.argv[2],"w").close()
            
            return

        binaryoutput.append(binary)
        pc+=4

        lineno+=1

    if len(sys.argv)>2:
        with open(sys.argv[2],"w") as f:
            for b in binaryoutput:
                f.write(b+"\n")
    else:
        for b in binaryoutput:
            print(b)

if __name__=="__main__":
    main()
