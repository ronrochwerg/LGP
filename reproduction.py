

# random uniform selection
def random_selection(pop, num_parent, rng, replacement = True):
    return rng.choice(pop, size = num_parent, replace = replacement)

# tournament selection, creates two tourneys, best fitness ind mutate or recombine to replace the losers in each tourney
# returns the indices of the winners and losers in the original population
def tourney_selection(pop, tourney_size, rng, replacement = False):

    #randomly select tourney individuals without replacement (for both tourneys)
    selected = rng.choice(len(pop), size = 2*tourney_size, replace=replacement)

    # split the individuals selected into two tourneys and sort them based on fitness
    tourney1 = sorted(selected[:tourney_size], key=lambda x: pop[x].fitness, reverse=True)
    tourney2 = sorted(selected[tourney_size:], key=lambda x: pop[x].fitness, reverse=True)

    #save winners and losers
    winners = [tourney1[0], tourney2[0]]
    losers = [tourney1[-1], tourney2[-1]]

    return winners, losers

def lexicase(pop, samples, target, num_return = 1):
    predictions = []
    for i, individual in enumerate(pop):
        prediction = individual.predict(samples)
        predictions.append([target - prediction,i])

    for i in range(len(samples)):
        min_err = min(predictions, key=lambda x: abs(x[0][i]))[0][i]
        predictions = [x for x in predictions if x[0][i] <= min_err]
        if len(predictions) == num_return:
            return pop[predictions[0][1]]
    return pop[predictions[0][1]]
