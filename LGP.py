from parameters import Parameters
from instruction import create_program
from mutation import apply_mutation
from recombination import apply_recombination
from evaluate import evaluate
from copy import copy


'''
Left to do: 
create print function for the program (create some extra parameters in param file for printing)
Add comments on other files
DO MAP ELITES

'''

# one linear genetic program
class LGP(object):

    # initialization of a single LGP individual, features is the number of features in the data
    def __init__(self, features):
        self.param = Parameters(features)
        self.instructions = []
        self.fitness = -1
        self.behavior = ""
        self.predictions = []

    # initialize an individual creating a random set of instructions using the initialization length
    def initialize(self):
        self.instructions = create_program(self.param)

    # sets fitness to the balanced accuracy, behavior to the error vector and predictions to the predictions on the
    # given data
    def evaluate(self, input_data, target_data):
        evaluation = evaluate(self.param, self.instructions, input_data, target_data)
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
        LGP_copy = LGP(self.param.num_features)
        LGP_copy.set_instructions(copy_instr)
        return LGP_copy

# add set instruction function for make copy


if __name__ == '__main__':
    testy = LGP(5)
    testy.initialize()
    print(testy.instructions)
    testy.mutate()
    print(testy.instructions)