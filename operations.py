# get the value of the operand in the instruction
def value(param, operand, sample):
    # if it is a constant, make it non-negative and return
    if operand < 0:
        return operand * -1
    # if it is a register, return its value
    elif operand < param.num_registers:
        return param.register_obj[operand].value
    # if it is a feature, return the correct one (they start counting after the number of registers)
    else:
        return sample[operand - param.num_registers]


# Executes the instruction
def apply_operation(param, instruction, sample):
    dest = instruction[0]
    src1 = value(param, instruction[1], sample)
    src2 = value(param, instruction[2], sample)
    op = instruction[3]
    if op == 0:
        param.register_obj[dest].value = src1 + src2
        return 1
    elif op == 1:
        param.register_obj[dest].value = src1 - src2
        return 1
    elif op == 2:
        param.register_obj[dest].value = src1 * src2
        return 1
    elif op == 3:
        if src2 != 0:
            param.register_obj[dest].value = src1 / src2
            return 1
        else:
            param.register_obj[dest].value = src1
            return 1
    elif op == 4:
        if src1 > src2:
            return 2
        else:
            return 1
    else:
        return -10**6