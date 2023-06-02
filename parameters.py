from .register import register
from numpy.random import default_rng

class Parameters:

    def __init__(self, features, rng):
        # list of operators and how many operators are being used
        self.operators_symbols = ['+','-','*','/','>']
        self.num_operators = len(self.operators_symbols)
        self.operators = list(range(self.num_operators))

        # program initialization length
        self.init_length = 15

        # program length bounds
        self.max_length = 60
        self.min_length = 10

        # list of constants (negative so that when storing them in instructions they can be differentiated from registers)
        self.constants = list(range(-1,-10, -1))

        # number of calculation registers
        self.num_registers = 10
        #creating the register objects
        self.register_obj = [register(i) for i in range(self.num_registers)]

        # number of features (only readable)
        self.num_features = features

        # number of all readable registers
        self.num_all = self.num_features + self.num_registers

        # creating lists for ease of random selection
        self.registers = list(range(self.num_registers))
        self.features = list(range(self.num_registers, self.num_features, 1))
        self.all_readable = list(range(self.num_all))

        # mutation rates
        self.mac_mut_rate = 0.5
        self.mic_mut_rate = 0.5

        self.recombination_type = "one_point_crossover"

        #maximum distance between crossover points
        self.max_dc = 10

        # rate of constant being used in instruction
        self.constant_rate = 0.5


        self.rng = rng