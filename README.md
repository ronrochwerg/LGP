
# LGP (Linear Genetic Programming)

This repository contains an implementation of Linear Genetic Programming (LGP)[[1]](#1). The key components include a set of parameters that control the behavior of the genetic programming algorithm and a class that represents individual genetic programs. This README provides an overview of the primary variables in the `parameters.py` file and the main functions in the `LGP.py` file.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Overview of Parameters](#overview-of-parameters)
- [Overview of LGP Class Functions](#overview-of-lgp-class-functions)
- [Contributing](#contributing)
<!--- [License](#license)-->

## Installation

To use this repository, it is currently necessary to clone it to your local machine:

```bash
git clone https://github.com/ronrochwerg/LGP.git
```

Make sure you have the required dependencies installed, which you can install via pip:

```bash
pip install -r requirements.txt
```
Note: we are currently in the process of adding this project to PyPI which will make installation easier.

## Usage

TBD

## Overview of Parameters

The `Parameters` class in `parameters.py` defines several key variables that influence the behavior of the genetic programming algorithm:

- **operators_symbols**: A list of symbols representing the operators used in the genetic program (`+`, `-`, `*`, `/`, `>`, `sin`, `cos`).
- **init_length**: A range of lengths for initializing programs, specified as `[min, max + 1]`.
- **max_length / min_length**: The maximum and minimum lengths allowed for a program.
- **constants**: A list of constant values used in the program, differentiated from registers by being negative.
- **evaluation_function**: The function used to evaluate the fitness of a program (`weighted_binary_cross_entropy`).
- **num_registers / num_features / num_all**: Various counts related to registers and features depending on whether input registers are separate (`input_sep`).
- **mutation rates**: `mac_mut_rate` and `mic_mut_rate` define the rates for macro and micro mutations.
- **recombination_type**: The type of crossover used in recombination, e.g., `one_point_crossover`.
- **max_dc**: Maximum distance allowed between crossover points in recombination.
- **constant_rate**: The rate at which constants are used in instructions.
- **effective_initialization / mutation / recombination**: Flags to enable effective initialization, mutation, and recombination (these are experimental and not fully implemented).

## Overview of LGP Class Functions

The `LGP` class in `LGP.py` represents an individual program in the genetic algorithm. Below are the main functions available in this class:

- **__init__**: Initializes a new LGP individual with the provided parameters.
- **initialize**: Randomly initializes an individual with a set of instructions.
- **evaluate**: Evaluates the fitness of the individual based on the input and target data.
- **predict**: Predicts outcomes based on the input data.
- **mutate**: Applies a mutation to the individual’s instructions.
- **recombine**: Applies crossover with another individual to produce offspring.
- **set_instructions**: Sets the instructions for an individual (useful for creating copies).
- **make_copy**: Creates and returns a copy of the individual.
- **print_program**: Prints the program's instructions and details in various formats (text, LaTeX).
- **complexity**: Computes and returns the complexity of the program.
- **print_parameters**: Prints the parameters associated with the individual.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.

<!--
## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
-->


## References

<a id="1">[1]</a> 
Brameier, Markus F., and Wolfgang Banzhaf. Basic concepts of linear genetic programming. Springer US, 2007.
