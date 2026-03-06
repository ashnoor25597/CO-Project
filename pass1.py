def pass1(assembly_code):
    symbol_table={}
    pc=0
    for line in assembly_code:
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            label=line.split(':',1)[0].strip()
            symbol_table[label]=pc
            parts=line.split(':',1)[1].strip()
            if parts:
                pc+=4
        else:
            pc+=4
    return symbol_table
