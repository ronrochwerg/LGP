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
        if instr[-1] == 4 and prev_eff:
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


