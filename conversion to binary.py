def toBinary(value,bits):
    num=int(value)
    if num<0:
        num=(1<<bits)+num
    binary=bin(num)[2:]
    return binary.zfill(bits)
