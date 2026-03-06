def check_label(my_label):

    if len(my_label)==0:
        return "Label is empty"
    
    if not my_label[0].isalpha():
        return "Invalid Label"
    
    for char in my_label:
        if not (char.isalnum() or char =="_"):
            return "Invalid Label"
        
    return True
