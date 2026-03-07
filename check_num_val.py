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
        
        convert_int(num)
    

    for char in num:
        if not char.isdigit():
            return False
        
    convert_int(num)
