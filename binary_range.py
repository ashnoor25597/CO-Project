def check_range(value):
    minimum=-(2**(12-1))
    maximum=(2**(12-1))-1

    if minimum<=value<=maximum:
        return True
    else:
        return False
