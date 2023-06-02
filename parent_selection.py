from numpy.random import default_rng

# random uniform selection
def random_selection(pop, num_parent, rng, replacement = True):
    return rng.choice(pop, size = num_parent, replace = replacement)

# tournament selection
def tourney_selection(pop, num_parent, tourney_size, rng, replacement = True):
    selected = []
    # keep tourney until all parents have been selected
    while len(selected) < num_parent:
        #randomly select tourney individuals without replacement
        tourney = rng.choice(pop, size = tourney_size, replacement=False)
        #find winner based on highest fitness
        winner = sorted(tourney, key=lambda x: x.fitness, reverse=True)[0]
        #if allowed replacement or the winner is not already selected add them to selection
        if replacement or winner not in selected:
            selected.append(winner)

    return selected
