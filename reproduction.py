

# random uniform selection
def random_selection(pop, num_parent, rng, replacement = True):
    return rng.choice(pop, size = num_parent, replace = replacement)

# tournament selection, creates two tourneys, best fitness ind mutate or recombine to replace the losers in each tourney
# returns the indices of the winners and losers in the original population
def tourney_selection(pop, tourney_size, rng, replacement = False):

    #randomly select tourney individuals without replacement (for both tourneys)
    selected = rng.choice(len(pop), size = 2*tourney_size, replacement=replacement)

    # split the individuals selected into two tourneys and sort them based on fitness
    tourney1 = sorted(selected[:tourney_size], key=lambda x: pop[x].fitness, reverse=True)
    tourney2 = sorted(selected[tourney_size:], key=lambda x: pop[x].fitness, reverse=True)

    #save winners and losers
    winners = [tourney1[0], tourney2[0]]
    losers = [tourney1[-1], tourney2[-1]]

    return winners, losers
