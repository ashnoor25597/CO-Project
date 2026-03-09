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