#from random import choice, random, shuffle
import re
from sympy import simplify, init_printing, latex, parse_expr, count_ops
# creating an instruction
def create_instruction(param, dest_options = None):
    # for effective instruction creation can specify a set to be chosen from for the destination register
    if dest_options:
        dest = param.rng.choice(list(dest_options))
    else:
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
def create_program(param, effective = False):
    length = param.rng.choice(param.init_length)
    # if initialization should be effective (all lines are effective)
    if effective:
        #build from the last instruction forward (reverse of intron deletion)
        eff_reg = {0}
        effective_reg = [[0]] #effective registers at this instruction (for macro mutation of insertion before the given instruction)
        instructions = []
        for i in range(length):
            instruction = create_instruction(param, eff_reg)
            print(eff_reg, instruction)
            eff_reg.remove(instruction[0])
            if 0 <= instruction[1] < param.num_registers:
                eff_reg.add(instruction[1])
            if 0 <= instruction[2] < param.num_registers:
                eff_reg.add(instruction[2])
            instructions.insert(0,instruction)
            effective_reg.insert(0, list(eff_reg))
        return instructions, effective_reg
    else:
        return [create_instruction(param) for _ in range(length)]

# to remove introns from a set of instructions
def intron_removal(param, instructions, effective = False):
    # keep track of efficient registers, instructions and if the previous instruction was efficient (for comparison operators)
    eff_reg = [False for i in param.registers]
    eff_reg[0] = True
    eff_reg_list = [[0]] #for macro mutation insertion (keeping track of effective registers)
    eff_list = []
    prev_eff = False

    # going through instructions in reverse order
    for instr in instructions[::-1]:
        # checking if the instruction is a comparison and if the previous instruction was efficient
        if instr[-1] == 4:
            if prev_eff:
                eff_list.append(instr)
                # Making registers true if they were used in the instruction (only for calc registers)
                if 0 <= instr[1] < param.num_registers:
                    eff_reg[instr[1]] = True
                if 0 <= instr[2] < param.num_registers:
                    eff_reg[instr[2]] = True
                if effective:
                    eff_reg_list.append([i for i,v in enumerate(eff_reg) if v]) # adding list of effective registers
                prev_eff = True
        elif eff_reg[instr[0]]:
            eff_list.append(instr)
            eff_reg[instr[0]] = False
            if 0 <= instr[1] < param.num_registers:
                eff_reg[instr[1]] = True
            if 0 <= instr[2] < param.num_registers:
                eff_reg[instr[2]] = True
            if effective:
                eff_reg_list.append([i for i, v in enumerate(eff_reg) if v])
            prev_eff = True
        else:
            prev_eff = False

    if effective:
        return eff_list[::-1], eff_reg_list[::-1]
    else:
        return eff_list[::-1]

def get_printable_value(param, src):
    if src < 0:
        return repr(src * -1)
    elif src < param.num_registers:
        return 'R' + repr(src)
    else:
        return 'INP' + repr(src - param.num_registers)

def print_instructions(param, instructions, lineage, effective = True, equation = False, file = None, print_latex = False):

    if effective:
        instructions = intron_removal(param, instructions)

    if equation:
        program = 'R0'
        for instruction in instructions[::-1]:
            program = program.replace(get_printable_value(param, instruction[0]),
                            '(' +get_printable_value(param, instruction[1]) + ' ' +
                            param.operators_symbols[instruction[3]] + ' ' +
                            get_printable_value(param, instruction[2]) + ')')
        if param.input_sep:
            # match any string with R and then any number of digits after and replace with a 1 since starting register
            # value is a 1
            program = re.sub(r"R\d+", '1', program)
        #have to do the replacement for non input separation

        expr = parse_expr(program)
        expr = simplify(expr)
        init_printing()
        print(expr, file=file)
        if print_latex:
            print('$' + latex(expr) + '$', file=file)

    else:
        print('Printing {effective} instructions for individual {lineage}'.format(effective= 'effective' if effective else 'all', lineage = lineage), file=file)
        for instruction in instructions:
            dest = 'R' + repr(instruction[0])
            src1 = get_printable_value(param, instruction[1])
            src2 = get_printable_value(param, instruction[2])
            op = instruction[3]
            if op == 4:
                print(src1, param.operators_symbols[op], src2 + ':', file=file)
            elif op == 5 or op == 6:
                print(dest, '=', param.operators_symbols[op] + '(' + src1 + ')', file=file)
            else:
                print(dest, '=', src1, param.operators_symbols[op], src2, file=file)

    print(file=file)

def get_complexity(param, instructions, reduced=True):
    instructions = intron_removal(param, instructions)

    program = 'R0'
    for instruction in instructions[::-1]:
        program = program.replace(get_printable_value(param, instruction[0]),
                                  '(' + get_printable_value(param, instruction[1]) + ' ' +
                                  param.operators_symbols[instruction[3]] + ' ' +
                                  get_printable_value(param, instruction[2]) + ')')
    if param.input_sep:
        # match any string with R and then any number of digits after and replace with a 1 since starting register
        # value is a 1
        program = re.sub(r"R\d+", '1', program)
    # have to do the replacement for non input separation

    expr = parse_expr(program)
    if reduced:
        expr = simplify(expr)
    return count_ops(expr, visual=False)