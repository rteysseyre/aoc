#!/usr/bin/env python3
# Raphaël Teysseyre, 2023

# Blizzard state. Contains tuples of (x, y, direction).
blizzards = set()

for y, l in enumerate(open('24_input').readlines()[1:-1]):
    for x, b in enumerate(l[1:-2]):
        if b == '.':
            continue
        blizzards.add((x, y, b))

xmax = max(map(lambda b: b[0], blizzards))
ymax = max(map(lambda b: b[1], blizzards))

def update_blizzard(b):
    if   b[2] == '>': new = [b[0] + 1, b[1], b[2]]
    elif b[2] == '<': new = [b[0] - 1, b[1], b[2]]
    elif b[2] == '^': new = [b[0], b[1] - 1, b[2]]
    elif b[2] == 'v': new = [b[0], b[1] + 1, b[2]]

    # Blizzards getting outside the valley bounds
    # reappear on the other side.
    if   new[0] < 0:    new[0] = xmax
    elif new[0] > xmax: new[0] = 0
    elif new[1] < 0:    new[1] = ymax
    elif new[1] > ymax: new[1] = 0

    return tuple(new)

def get_blizzard_coords(b):
    return b[:2]

def get_possible_steps(p):
    test = [(p[0] - 1, p[1]), (p[0] + 1, p[1]),
            (p[0], p[1] - 1), (p[0], p[1] + 1)]

    out = []
    for t in test:
        # Check for steps going outside the valley
        if (t[0] >= 0 and t[0] <= xmax and
            t[1] >= 0 and t[1] <= ymax):
            out.append(t)

    # Don't forget that we can choose to stay in place
    return [p] + out

# Returns a tuble of (new blizzard state, new possible positions)
# from a current blizzard state and a set of current possible positions.
def step(b, curr):
    # Update blizzards
    new_b = set(map(update_blizzard, b))
    new_b_coords = set(map(get_blizzard_coords, new_b))

    # Find possible new positions
    out = set()
    for c in curr:
        for cc in get_possible_steps(c):
            if cc not in new_b_coords:
                out.add(cc)

    return (new_b, out)

# Breadth-first search to find the fastest path to the target
def find_shortest_path(blizzards, start, almost_target):
    i = 0
    positions = {start}
    while almost_target not in positions:
        blizzards, positions = step(blizzards, positions)
        i += 1

    # One more step to get to the actual goal outside of the valley
    blizzards, positions = step(blizzards, positions)
    return (blizzards, i + 1)

# Part 1
blizzards, count1 = find_shortest_path(blizzards, (0, -1), (xmax, ymax))
print(count1)

# Part 2
blizzards, count2 = find_shortest_path(blizzards, (xmax, ymax + 1), (0, 0))
blizzards, count3 = find_shortest_path(blizzards, (0, -1), (xmax, ymax))
print(count1 + count2 + count3)
