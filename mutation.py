from random import sample, randint, choice, random
from instruction import create_instruction

# Apply a mutation to a set of LGP instructions. This function guarantees a mutation and allows for both micro and macro
# at the same time
def apply_mutation(param, instructions):
    new_instr = instructions
    change = False
    # We never want to return instructions that have not mutated in some way
    while not change:
        if random() < param.mac_mut_rate:
            new_instr = macro_mut(param, new_instr)
            change = True
        if random() < param.mic_mut_rate:
            new_instr = micro_mut(param, new_instr)
            change = True
    return new_instr


# Apply a micro-mutation which changes a value in an instruction
def micro_mut(param, instructions, num_mut=1):
    places = sample(range(0, len(instructions) - 1), num_mut)
    for place in places:
        replace = randint(0, 3)
        # replacing the destination
        if replace == 0:
            instructions[place][replace] = choice(
                [i for i in param.registers if i is not instructions[place][replace]])
        # replacing the first operand
        elif replace == 1:
            # if the other operand is not a constant and passes the constant rate, change it for a constant
            if instructions[place][2] > 0 and random() < param.constant_rate:
                instructions[place][replace] = choice(param.constants)
            # if the other operand is a constant or if it does not pass the constant rate, replace it with a register
            else:
                instructions[place][replace] = choice(
                    [i for i in param.all_readable if i is not instructions[place][replace]])
        # replacing the second operand
        elif replace == 2:
            if instructions[place][2] > 0 and random() < param.constant_rate:
                instructions[place][replace] = choice(param.constants)
            else:
                instructions[place][replace] = choice(
                    [i for i in param.all_readable if i is not instructions[place][replace]])
        else:
            instructions[place][replace] = choice(
                [i for i in param.operators if i is not instructions[place][replace]])

    return instructions

# Apply a macro-mutation which adds, deletes or replaces an instruction
def macro_mut(param, instructions, threshold = (0.33,0.66,1)):
    chosen_mut = random()

    if chosen_mut < threshold[0] and len(instructions) < param.max_length: # insertion
        new_instr = create_instruction(param)
        place = randint(0, len(instructions))
        instructions.insert(place, new_instr)
    elif chosen_mut < threshold[1] and len(instructions) > param.min_length: # deletion
        place = randint(0, len(instructions) - 1)
        del instructions[place]
    else: # replacement
        new_instr = create_instruction(param)
        place = randint(0, len(instructions) - 1)
        instructions[place] = new_instr

    return instructions