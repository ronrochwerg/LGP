# for ignoring sklearn warning about different subclass in y-predicted
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
from sklearn.metrics import balanced_accuracy_score
from .operations import apply_operation
from .instruction import intron_removal
import numpy as np

# calculating the balanced accuracy given a set of predictions and true values
def balanced_accuracy(target_data, predictions):
    strict_pred = [-1 if x < 0 else 1 if x > 0 else 0 for x in predictions]
    return balanced_accuracy_score(target_data, strict_pred)


# For evaluating the set of instructions on a set of data, can return the balanced accuracy, raw predictions, or error vector.
def evaluate(param, instructions, input_data, target_data):
    # getting the effective instructions
    reduced_instr = intron_removal(param, instructions)
    predictions = []
    # going through each sample in the data and getting the prediction
    if len(reduced_instr) > 0:
        for sample in input_data:
            pred_val = np.tanh(eval_sample(param, reduced_instr, sample))
            # for binary problems (0 return counts as undecided and is wrong no matter what)
            predictions.append(pred_val)
            # if pred_val > 0:
            #     predictions.append(1)
            # elif pred_val < 0:
            #     predictions.append(-1)
            # else:
            #     predictions.append(0)
    # if the program has no effective instructions then it gets all samples incorrect
    else:
        predictions = [0] * len(target_data)

    error_vect = target_data - predictions
    return [balanced_accuracy(target_data, predictions), np.array(error_vect), predictions]

# run a single sample through a set of LGP instructions
def eval_sample(param, instructions, sample):
    instr = 0
    while 0 <= instr < len(instructions):
        instr += apply_operation(param, instructions[instr], sample)

    return param.register_obj[0].value

