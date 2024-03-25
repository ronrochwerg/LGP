# for ignoring sklearn warning about different subclass in y-predicted
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
warnings.filterwarnings('ignore')
from sklearn.metrics import balanced_accuracy_score
from .operations import apply_operation
from .instruction import intron_removal
import numpy as np

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

# calculating the balanced accuracy given a set of predictions and true values
def balanced_accuracy(target_data, predictions):
    strict_pred = [0 if x < 0.5 else 1 if x > 0.5 else -1 for x in predictions]
    return balanced_accuracy_score(target_data, strict_pred)

def weighted_binary_cross_entropy(target_data, predictions, weights):
    loss_vals = [target_data[i]*np.log(predictions[i])*weights[i] + (1-target_data[i])*(np.log(1-predictions[i]))*weights[i] for i in range(len(target_data))]
    loss = -1*sum(loss_vals)
    if np.isnan(loss):
        return float('inf')
    return -1*sum(loss_vals)


# For evaluating the set of instructions on a set of data, can return the balanced accuracy, raw predictions, or error vector.
def evaluate(param, registers, instructions, input_data, target_data, weights=None, effective = False):
    # getting the effective instructions
    if weights is None:
        weights = [1] * len(target_data)
    if effective:
        reduced_instr, eff_reg = intron_removal(param, instructions, effective)
    else:
        reduced_instr = intron_removal(param, instructions, effective)
    predictions = []
    # going through each sample in the data and getting the prediction
    if len(reduced_instr) > 0:
        for sample in input_data:
            pred_val = sigmoid(eval_sample(param, registers, reduced_instr, sample))
            # pred_val = eval_sample(param, registers, reduced_instr, sample)
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
        predictions = [-1] * len(target_data)
    error_vect = target_data - predictions
    if effective:
        return [weighted_binary_cross_entropy(target_data, predictions, weights), np.array(error_vect), predictions, reduced_instr, eff_reg]
    else:
        return [weighted_binary_cross_entropy(target_data, predictions, weights), np.array(error_vect), predictions]

def predict(param, registers, instructions, input_data, sig = True):
    # getting the effective instructions
    reduced_instr = intron_removal(param, instructions)
    predictions = []
    # going through each sample in the data and getting the prediction
    if len(reduced_instr) > 0:
        for sample in input_data:
            if sig:
                pred_val = sigmoid(eval_sample(param, registers, reduced_instr, sample))
            else:
                pred_val = eval_sample(param, registers, reduced_instr, sample)
            predictions.append(pred_val)

    # if the program has no effective instructions then it gets all samples incorrect
    else:
        predictions = [0] * len(input_data)

    return predictions

# run a single sample through a set of LGP instructions
def eval_sample(param, registers, instructions, sample):
    instr = 0
    # resetting the values in the calculation registers
    if param.input_sep: # if features are read only
        for register in registers:
            register.value = 1
    else: # if features are same as calc registers
        for i, register in enumerate(registers):
            register.value = sample[i%len(sample)]

    while 0 <= instr < len(instructions):
        instr += apply_operation(param, registers, instructions[instr], sample)

    return registers[0].value

