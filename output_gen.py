def output(binary_txt):
    
    output_lines=[]

    output_lines.append(binary_txt)

    with open(sys.argv[2], "w") as f:
        for line in output_lines:
            f.write(line+"\n")