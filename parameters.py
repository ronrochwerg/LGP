from .register import register
from json import dumps

from .evaluate import weighted_binary_cross_entropy
from .recombination import one_point_crossover

class Parameters:

    def __init__(self, num_features, rng, input_sep = True):
        # list of operators and how many operators are being used
        self.operators_symbols = ['+','-','*','/','>','sin', 'cos']
        self.operators = [0,1,2,3,4,5,6]
        self.num_operators = len(self.operators)

        # program initialization length ([min, max + 1])
        self.init_length = list(range(10,16))

        # program length bounds
        self.max_length = 60
        self.min_length = 10

        # list of constants (negative so that when storing them in instructions they can be differentiated from registers)
        self.constants = list(range(-1,-10, -1))

        self.evaluation_function = weighted_binary_cross_entropy

        self.input_sep = input_sep
        # different parameters for if there are separate readable input registers (otherwise calc registers hold the input)
        if input_sep:
            # number of calculation registers
            self.num_registers = 4

            # number of features (only readable)
            self.num_features = num_features

            # number of all readable registers
            self.num_all = self.num_features + self.num_registers

            # creating lists for ease of random selection
            self.registers = list(range(self.num_registers))
            self.features = list(range(self.num_registers, self.num_all, 1))
            self.all_readable = list(range(self.num_all))
        else:
            # number of calculation registers
            self.num_registers = num_features

            # number of features (only readable)
            self.num_features = num_features

            # number of all readable registers
            self.num_all = num_features

            # creating lists for ease of random selection
            self.registers = list(range(self.num_registers))
            self.features = list(range(self.num_registers))
            self.all_readable = list(range(self.num_all))

        # mutation rates
        self.mac_mut_rate = 0.5
        self.mic_mut_rate = 0.5

        self.recombination_type = one_point_crossover

        #maximum distance between crossover points
        self.max_dc = 10

        # rate of constant being used in instruction
        self.constant_rate = 0.5

        # random number generator
        self.rng = rng

        # for effective initialization of programs
        # work in progress, not ready to be used yet
        self.effective_initialization = False
        self.effective_mutation = False
        self.effective_recombination = False

    def print_attributes(self, file=None):
        for k,v in vars(self).items():
            print('{}: \t {}'.format(k,v), file=file)