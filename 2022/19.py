#!/usr/bin/env python3
# Raphaël Teysseyre, 2023

# Used reddit for optimization ideas (don't hoard resources
# when a robot can be built, don't build a robot if we can't
# absorb it's production, prune states that have no chance
# of catching up with the current-best).

import re
import numpy as np
import time

# Order of numbers in the input file
BP_ORE_COST = 1
BP_CLAY_COST = 2
BP_OBS_COST_ORE = 3
BP_OBS_COST_CLAY = 4
BP_GE_COST_ORE = 5
BP_GE_COST_OBS = 6

blueprints = [[int(x) for x in re.findall('\d+', l)] for l in open('19_input')]

# Return the cost structure for a blueprint as a tuple
# The first four elements of the tuple give the (ore, clay, obsidian)
# cost of each type of robot (ore, clay, obsidian, geode in that order).
# The last element of the tuple gives the maximum cost for each resource.
def get_costs(bp):
    return ((bp[BP_ORE_COST], 0, 0),
            (bp[BP_CLAY_COST], 0, 0),
            (bp[BP_OBS_COST_ORE], bp[BP_OBS_COST_CLAY], 0),
            (bp[BP_GE_COST_ORE], 0, bp[BP_GE_COST_OBS]),
            (max(bp[BP_ORE_COST],
                 bp[BP_CLAY_COST],
                 bp[BP_OBS_COST_ORE],
                 bp[BP_GE_COST_ORE]),
             bp[BP_OBS_COST_CLAY],
             bp[BP_GE_COST_OBS]))

# The state is a vector containing 8 elements.
# The first four elements are the resource counts (in ore, clay, obsidian, geode order),
# The last four elements are the robot counts (same order).
def get_possible_transitions(curr, costs):
    resources = curr[:4]
    robots = curr[4:]
    new_resources = [re + ro for re, ro in zip(resources, robots)]

    if all([n >= m for n,m in zip(resources, costs[4])]):
        # All resources are above the maximum cost,
        # We should build a robot instead of hoarding resources
        out = []
    else:
        out = [new_resources + robots]

    for i in range(4):
        if i < 3 and robots[i] >= costs[4][i]:
            # No need to build this robot, we would not be able
            # to absorb the production
            continue

        if all(r >= c for r, c in zip(resources[:3], costs[i])):
            new_robots = [0, 0, 0, 0]
            new_robots[i] = 1

            out.append([r - c for r, c in zip(new_resources, costs[i] + (0,))]
                       + [r + n for r, n in zip(robots, new_robots)])

    return out

# Prune state that have both less resources and
# less robots than another state.
def prune_less_performing(v):
    out = []
    for i, v1 in enumerate(v):
        for v2 in v[i+1:]:
            if all(a <= b for a,b in zip(v1, v2)):
                # Discard v1.
                break
        else:
            out.append(v1)
    return out

# Prune states for which we can easily prove that
# they have no chance of catching-up with the current
# best state.
def prune_if_no_chance(v, remaining_time):
    # How many geodes can the best state produce,
    # Assuming no new geode robot is built?
    best = 0
    for x in v:
        test = x[3] + x[7] * remaining_time
        if test > best:
            best = test

    # How many additional geodes can be produced, assuming
    # we create one new geode robot on each time slot?
    max_new = remaining_time * (remaining_time - 1) / 2

    out = []
    for x in v:
        if x[3] + x[7] * remaining_time + max_new >= best:
            # This state has a chance of catching-up with the
            # current best state.
            out.append(x)

    return out    

# Breadth-first search
def get_possible_results(curr, costs, remaining_time):
    if remaining_time == 0 or len(curr) == 0:
        return curr

    nxt = []
    for x in curr:
        nxt += get_possible_transitions(x, costs)

    nxt = prune_if_no_chance(nxt, remaining_time)
    
    if len(nxt) < 1000: # Otherwise it's too slow
        nxt = prune_less_performing(nxt)

    return get_possible_results(nxt, costs, remaining_time - 1)

# Return the geode count for a blueprint running for a specific time
def get_geode_count(bp, time):
    res = get_possible_results([[0, 0, 0, 0, 1, 0, 0, 0]],
                               get_costs(bp), time)
    best = 0
    for c in res:
        if c[3] > best:
            best = c[3]

    return best

# Part 1
total = 0
for i, bp in enumerate(blueprints):
    c = get_geode_count(bp, 24)
    print('Blueprint ', i + 1, ', max geodes: ', c)
    total += (i + 1) * c
print('Part 1 answer:', total)

# Part 2
total = 1
for i, bp in enumerate(blueprints[:3]):
    c = get_geode_count(bp, 32)
    print('Blueprint ', i + 1, ', max geodes: ', c)
    total *= c
print('Part 2 answer:', total)
