def check_range(value, bits):
    minimum=-(2**(bits-1))
    maximum=(2**(bits-1))-1

    if minimum<=value<=maximum:
        return True
    else:
        return False
