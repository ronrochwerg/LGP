from operations import apply_operation
from instruction import intron_removal

# calculating the balanced accuracy given a set of predictions and true values
def balanced_accuracy(predictions, target_data):
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for i in range(len(predictions)):
        if predictions[i] == target_data[i] == 1:
            TP += 1
        elif predictions[i] == target_data[i] == 0:
            TN += 1
        elif predictions[i] == 1:
            FP += 1
        elif predictions[i] == 0:
            FN += 1
        elif target_data[i] == 0:  # when prediction is -1
            FP += 1
        elif target_data[i] == 1:  # when prediction is -1
            FN += 1
    balanced_acc = 0.5 * (TP / (TP + FN)) + 0.5 * (TN / (TN + FP))

    return balanced_acc

# For evaluating the set of instructions on a set of data, can return the balanced accuracy, raw predictions, or error vector.
def evaluate(param, instructions, input_data, target_data):
    # getting the effective instructions
    reduced_instr = intron_removal(param, instructions)
    predictions = []

    # going through each sample in the data and getting the prediction
    if len(reduced_instr) > 0:
        for sample in input_data:
            pred_val = eval_sample(param, reduced_instr, sample)
            # for binary problems (0 return counts as undecided and is wrong no matter what)
            if pred_val > 0:
                predictions.append(1)
            elif pred_val < 0:
                predictions.append(0)
            else:
                predictions.append(-1)
    # if the program has no effective instructions then it gets all samples incorrect
    else:
        predictions = [-1] * len(target_data)

    error_vect = [1 if predictions[i] == target_data[i] else 0 for i in range(len(predictions))]
    return [balanced_accuracy(predictions, target_data), repr(error_vect), predictions]

# run a single sample through a set of LGP instructions
def eval_sample(param, instructions, sample):
    instr = 0
    while 0 <= instr < len(instructions):
        instr += apply_operation(param, instructions[instr], sample)

    return param.register_obj[0].value

