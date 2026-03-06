def check_range(value):
    min=-(2**(12-1))
    max=(2**(12-1))-1

    if min<=value<=max:
        return True
    else:
        return False
