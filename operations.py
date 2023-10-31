from numpy import sqrt, sin, cos
# get the value of the operand in the instruction
def value(param, registers, operand, sample):
    # if it is a constant, make it non-negative and return
    if operand < 0:
        return operand * -1
    # if it is a register, return its value
    elif operand < param.num_registers:
        return registers[operand].value
    # if it is a feature, return the correct one (they start counting after the number of registers)
    else:
        return sample[operand - param.num_registers]


# Executes the instruction
def apply_operation(param, registers, instruction, sample):
    dest = instruction[0]
    src1 = value(param, registers, instruction[1], sample)
    src2 = value(param, registers, instruction[2], sample)
    op = instruction[3]
    #addition
    if op == 0:
        registers[dest].value = src1 + src2
        return 1
    #subtraction
    elif op == 1:
        registers[dest].value = src1 - src2
        return 1
    #multiplication
    elif op == 2:
        registers[dest].value = src1 * src2
        return 1
    #protected division
    elif op == 3:
        if src2 == 0:
            return 1
        else:
            registers[dest].value = src1/src2
            return 1
    #branch
    elif op == 4:
        if src1 > src2:
            return 2
        else:
            return 1
    elif op == 5:
        registers[dest].value = sin(src1)
        return 1
    elif op == 6:
        registers[dest].value = cos(src1)
        return 1
    #just in case
    else:
        exit('error in applying operation, incorrect operation value')


if __name__ == '__main__':
    print('operations')