#from random import choice, random, shuffle

# creating an instruction
def create_instruction(param):
    # choosing destination register
    dest = param.rng.choice(param.registers)

    # choosing if instruction will have a constant or not
    if param.rng.random() < param.constant_rate:
        const = param.rng.choice(param.constants)
        other = param.rng.choice(param.all_readable)
        out = [const, other]
        param.rng.shuffle(out)
        src1 = out[0]
        src2 = out[1]
    else:
        src1 = param.rng.choice(param.all_readable)
        src2 = param.rng.choice(param.all_readable)
    op = param.rng.choice(param.operators)
    return [dest, src1, src2, op]

# creating a program with the initial program length
def create_program(param):
     return [create_instruction(param) for i in range(param.init_length)]

# to remove introns from a set of instructions
def intron_removal(param, instructions):
    # keep track of efficient registers, instructions and if the previous instruction was efficient (for comparison operators)
    eff_reg = [False for i in param.registers]
    eff_reg[0] = True
    eff_list = []
    prev_eff = False

    # going through instructions in reverse order
    for instr in instructions[::-1]:
        # checking if the instruction is a comparison and if the previous instruction was efficient
        if instr[-1] == 4:
            if prev_eff:
                eff_list.append(instr)
                # Making registers true if they were used in the instruction (only for calc registers)
                if 0 < instr[1] < param.num_registers:
                    eff_reg[instr[1]] = True
                if 0 < instr[2] < param.num_registers:
                    eff_reg[instr[2]] = True
                prev_eff = True
        elif eff_reg[instr[0]]:
            eff_list.append(instr)
            eff_reg[instr[0]] = False
            if 0 < instr[1] < param.num_registers:
                eff_reg[instr[1]] = True
            if 0 < instr[2] < param.num_registers:
                eff_reg[instr[2]] = True
            prev_eff = True
        else:
            prev_eff = False

    return eff_list[::-1]

def get_printable_value(param, src):
    if src < 0:
        return repr(src * -1)
    elif src < param.num_registers:
        return 'R' + repr(src)
    else:
        return 'INP' + repr(src - param.num_registers)

def print_instructions(param, instructions, lineage, effective = False):

    if effective:
        instructions = intron_removal(param, instructions)

    print('Printing {effective} instructions for individual {lineage}'.format(effective= 'effective' if effective else 'all', lineage = lineage))
    for instruction in instructions:
        dest = 'R' + repr(instruction[0])
        src1 = get_printable_value(param, instruction[1])
        src2 = get_printable_value(param, instruction[2])
        op = instruction[3]
        if op == 4:
            print(src1, param.operators_symbols[op], src2 + ':')
        elif op == 5 or op == 6:
            print(dest, '=', param.operators_symbols[op] + '(' + src1 + ')')
        else:
            print(dest, '=', src1, param.operators_symbols[op], src2)

    print()


