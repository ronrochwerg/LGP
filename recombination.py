#from random import randint

def one_point_crossover(param, instruction_1, instruction_2):
    len1 = len(instruction_1)
    len2 = len(instruction_2)

    # making sure instruction 1 is the smaller program
    if len1 > len2:
        instruction_1, instruction_2 = instruction_2, instruction_1
        len1, len2 = len2, len1

    # choosing crossover points
    p1 = param.rng.integers(low=1, high=len(instruction_1) - 1, endpoint=True)
    #making sure second point is within maximum distance
    p2 = param.rng.integers(low=max(1, p1 - param.max_dc), high=min(len(instruction_2)-1,p1 + param.max_dc), endpoint=True)

    len_s1 = len(instruction_1) - p1
    len_s2 = len(instruction_2) - p2

    if len_s1 <= len_s2:
        if len(instruction_2) - (len_s2 - len_s1) < param.min_length or len(instruction_1) + (len_s2 -len_s1) > param.max_length:
            p2 = p1
    else:
        if len(instruction_1) + (len_s2 - len_s1) < param.min_length or  len(instruction_2) - (len_s2 - len_s1) > param.max_length:
            p2 = p1

    new_inst_1 = instruction_1[:p1] + instruction_2[p2:]
    new_inst_2 = instruction_2[:p2] + instruction_1[p1:]

    return new_inst_1, new_inst_2