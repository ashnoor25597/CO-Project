def convert_int(num):
    
    
    if num.startswith("0x") or num.startswith("0X") or num.startswith("-0x") or num.startswith("-0X"):
        return int(num, 16)    
    
    if num.startswith("-"):
        return int(num)
    
    return int(num)