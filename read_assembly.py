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
