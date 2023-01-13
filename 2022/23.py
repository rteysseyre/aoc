#!/usr/bin/env python3
# Raphaël Teysseyre, 2023

# Store elf positions as a 32-bit positive integer,
# to make looking for positions in a set faster.
# Higher 16 bits are the x position plus 1 << 15,
# Lower 16 bits are the y position plus 1 << 15.

# (tuple) Position to int
def posint(x, y):
    assert y < 32768
    assert y > -32769
    return (x + (1 << 15)) << 16 | (y + (1 << 15))

# (int) position to tuple
def postup(a):
    return ((a >> 16) - (1 << 15), (a & 0xFFFF) - (1 << 15))

elf_positions = []

for y, l in enumerate(open('23_input').readlines()):
    for x, c in enumerate(l[:-1]):
        if c == '#':
            elf_positions.append(posint(x, y))

proposal_order = ['N', 'S', 'W', 'E']

def has_neighbours(pos, elf_positions_set):
    # Position of all 8 neighbours
    test_pos = [pos - 65537,
                pos - 1,
                pos + 65535,
                pos - 65536,
                pos + 65536,
                pos - 65535,
                pos + 1,
                pos + 65537]

    neighbours = [p in elf_positions_set for p in test_pos]
    return { 'all': any(neighbours),
             'N': any(neighbours[:3]),
             'S': any(neighbours[5:]),
             'W': any([neighbours[0], neighbours[3], neighbours[5]]),
             'E': any([neighbours[2], neighbours[4], neighbours[7]]) }

def get_new_pos(pos, direction):
    if direction == 'N':
        return pos - 1
    elif direction == 'S':
        return pos + 1
    elif direction == 'W':
        return pos - 65536
    elif direction == 'E':
        return pos + 65536

# Returns a tuple of (new_elf_positions, bool),
# with the boolean indicating if at least one
# elf has moved in this step
def step(elf_positions):
    # In Python, the "in" operation on sets is faster
    # than on lists. Pass a set to has_neighbour() instead
    # of the elf_positions_list, this is faster.
    ep_set = set(elf_positions)
    proposed_positions = []
    for e in elf_positions:
        hn = has_neighbours(e, ep_set)
        if not hn['all']:
            # No neighbour, don't move
            proposed_positions.append(e)
            continue

        for d in proposal_order:
            if not hn[d]:
                # No neighbour in that direction, move
                proposed_positions.append(get_new_pos(e, d))
                break
        else:
            # Neighbours everywhere, don't move
            proposed_positions.append(e)

    new_positions = []
    for i, p in enumerate(proposed_positions):
        if p in proposed_positions[:i] + proposed_positions[i+1:]:
            # Another elf wants to move to our proposed position. Don't move.
            new_positions.append(elf_positions[i])
        else:
            new_positions.append(p)

    return (new_positions, any([a != b for a,b in zip(elf_positions, new_positions)]))

def get_extent(elf_positions):
    min_x = postup(elf_positions[0])[0]
    min_y = postup(elf_positions[0])[1]
    max_x = postup(elf_positions[0])[0]
    max_y = postup(elf_positions[0])[1]

    for p in elf_positions:
        e = postup(p)
        if e[0] > max_x:
            max_x = e[0]
        elif e[0] < min_x:
            min_x = e[0]
        if e[1] > max_y:
            max_y = e[1]
        elif e[1] < min_y:
            min_y = e[1]

    return {'min_x': min_x, 'max_x': max_x, 'min_y': min_y, 'max_y': max_y}

# Part 1
for i in range(10):
    (elf_positions, moved) = step(elf_positions)
    proposal_order = proposal_order[1:] + [proposal_order[0]]

extent = get_extent(elf_positions)

print((extent['max_x'] - extent['min_x'] + 1)
      * (extent['max_y'] - extent['min_y'] + 1)
      - len(elf_positions))

# Part 2
# We already did 10 steps to solve part 1. Continue from there.
step_count = 10

while moved:
    (elf_positions, moved) = step(elf_positions)
    proposal_order = proposal_order[1:] + [proposal_order[0]]
    step_count += 1
    if step_count % 50 == 0:
        print('Total steps:', step_count)

print('Total steps:', step_count)
