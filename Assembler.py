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