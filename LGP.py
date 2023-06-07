from .parameters import Parameters
from .instruction import create_program
from .mutation import apply_mutation
from .recombination import apply_recombination
from .evaluate import evaluate
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
        self.fitness = -1
        self.behavior = ""
        self.predictions = []
        self.register_obj = [register(i) for i in range(self.param.num_registers)]

    # initialize an individual creating a random set of instructions using the initialization length
    def initialize(self):
        self.instructions = create_program(self.param)

    # sets fitness to the balanced accuracy, behavior to the error vector and predictions to the predictions on the
    # given data
    # input data should be a list of lists, target data should be a list of values (targets)
    def evaluate(self, input_data, target_data):
        evaluation = evaluate(self.param, self.register_obj, self.instructions, input_data, target_data)
        self.fitness = evaluation[0]
        self.behavior = evaluation[1]
        self.predictions = evaluation[2]

    # applies a mutation to the individual (directly to the individual)
    def mutate(self):
        self.instructions = apply_mutation(self.param,self.instructions)

    # applies recombination to the individual and another individual (directly, should already be copies)
    def recombine(self, other):
        child1, child2 = apply_recombination(self.param, self.instructions, other.instructions)
        self.set_instructions(child1)
        other.set_instructions(child2)

    # function for setting the instructions of an individual (used for creating copies)
    def set_instructions(self, instructions):
        self.instructions = instructions

    # function for making a copy of an individual (blank individual with the same instructions)
    def make_copy(self):
        copy_instr = [copy(i) for i in self.instructions]
        LGP_copy = LGP(self.param)
        LGP_copy.set_instructions(copy_instr)
        return LGP_copy

    def mutate_child(self, input_data, target_data):
        child = self.make_copy()
        child.mutate()
        child.evaluate(input_data, target_data)
        return child

    def recombine_child(self, other, input_data, target_data):
        child1 = self.make_copy()
        child2 = other.make_copy()
        child1.recombine(child2)
        child1.evaluate(input_data, target_data)
        child2.evaluate(input_data, target_data)
        return child1, child2

# add set instruction function for make copy


if __name__ == '__main__':

    testy = LGP(5)
    testy.initialize()

    testy2 = LGP(5)
    testy2.initialize()

    print(testy.instructions)
    print(testy2.instructions)

    child1, child2 = testy.recombine_child(testy2, np.array([[1,2,3,4,5]]), np.array([1]))

    print(child1.instructions)
    print(child2.instructions)

    print(testy == testy)
    print(testy == testy2)
    print(testy == testy.make_copy())

    listy = []

    print(listy.count(testy) == len(listy))
