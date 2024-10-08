from .parameters import Parameters
from .instruction import create_program, print_instructions, get_complexity
from .mutation import apply_mutation
from .evaluate import evaluate, predict
from .register import register
from copy import copy
import numpy as np


'''
Left to do: 
create print function for the program (create some extra parameters in param file for printing)
Add comments on other files

'''

# one linear genetic program
class LGP(object):

    # initialization of a single LGP individual, features is the number of features in the data
    def __init__(self, param):
        self.param = param
        self.instructions = []
        self.effective_registers = []
        self.fitness = -1
        self.predictions = []
        self.register_obj = [register(i) for i in range(self.param.num_registers)]

        self.num_children = 0
        self.lineage = '0'

    # initialize an individual creating a random set of instructions using the initialization length
    def initialize(self, input_data, target_data, weights=None, name = '0'):
        if self.param.effective_initialization:
            self.instructions, self.effective_registers = create_program(self.param, self.param.effective_initialization)
        else:
            self.instructions = create_program(self.param, self.param.effective_initialization)
        self.evaluate(input_data, target_data, weights=weights, effective=self.param.effective_initialization)
        self.lineage = repr(name)

    # sets fitness to the balanced accuracy, behavior to the error vector and predictions to the predictions on the
    # given data
    # input data should be a list of lists, target data should be a list of values (targets) (both should be np arrays)
    def evaluate(self, input_data, target_data, weights=None, effective=False):
        evaluation = evaluate(self.param, self.register_obj, self.instructions, input_data, target_data, weights=weights, effective=effective)
        if effective:
            self.instructions = evaluation[3]
            self.effective_registers = evaluation[4]
        self.fitness = evaluation[0]
        self.predictions = evaluation[1]

    def predict(self, input_data, sig=True):
        return predict(self.param, self.register_obj, self.instructions, input_data, sig)

    # applies a mutation to the individual (directly to the individual)
    def mutate(self):
        self.instructions = apply_mutation(self.param,self.instructions, self.effective_registers)

    # applies recombination to the individual and another individual (directly, should already be copies)
    def recombine(self, other):
        child1, child2 = self.param.recombination_type(self.param, self.instructions, other.instructions)
        self.set_instructions(child1)
        other.set_instructions(child2)

    # function for setting the instructions of an individual (used for creating copies)
    def set_instructions(self, instructions):
        self.instructions = instructions

    # function for making a copy of an individual (blank individual with the same instructions)
    def make_copy(self):
        self.num_children += 1
        copy_instr = [copy(i) for i in self.instructions]
        LGP_copy = LGP(self.param)
        LGP_copy.set_instructions(copy_instr)
        LGP_copy.lineage = self.lineage + ',' + repr(self.num_children)
        return LGP_copy

    # used for directly making children through mutation or recombination
    # (same as making a copy and then mutating/recombining the copies)
    # def mutate_child(self, input_data, target_data):
    #     child = self.make_copy()
    #     child.mutate()
    #     child.evaluate(input_data, target_data, effective=self.param.effective_mutation)
    #     return child
    #
    # def recombine_child(self, other, input_data, target_data):
    #     child1 = self.make_copy()
    #     child2 = other.make_copy()
    #     child1.recombine(child2)
    #     child1.evaluate(input_data, target_data, effective=self.param.effective_recombination)
    #     child2.evaluate(input_data, target_data, effective=self.param.effective_recombination)
    #     return child1, child2

    def print_program(self, effective = True, equation = False, file = None, print_latex = False):
        print_instructions(self.param, self.instructions, self.lineage, effective = effective, equation = equation,
                           file = file, print_latex = print_latex)

    def complexity(self, reduced = True):
        return get_complexity(self.param, self.instructions, reduced=reduced)

    def print_parameters(self, file = None):
        self.param.print_attributes(file = file)

# add set instruction function for make copy

