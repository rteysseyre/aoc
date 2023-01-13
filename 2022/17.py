#!/usr/bin/env python3
# Raphaël Teysseyre, 2023

# Rock shapes
rocks = [{(0,0), (1,0), (2,0), (3,0)},
         {(1,0), (0,1), (1,1), (2,1), (1,2)},
         {(0,0), (1,0), (2,0), (2,1), (2,2)},
         {(0,0), (0,1), (0,2), (0,3)},
         {(0,0), (0,1), (1,0), (1,1)}]

pattern = open('17_input').readlines()[0].strip()

def coords_move(coords, x, y):
    return (coords[0] + x, coords[1] + y)

def coords_set_move(r, x, y):
    return set(map(lambda c : coords_move(c, x, y), r))

def valid_coords(coords):
    return coords[0] >= 0 and coords[0] < 7 and coords not in floor

def valid_rock(r):
    return all(map(valid_coords, r))

# Simulate a rock falling
def fall_rock(r):
    global floor
    global floor_highest
    global pattern_index
    global pattern

    # Move rock to initial position
    r = coords_set_move(r, 2, floor_highest + 4)
    while 1:
        # Move rock sideways
        if pattern[pattern_index] == '<':
            r_moved = coords_set_move(r, -1, 0)
        else:
            r_moved = coords_set_move(r, 1, 0)

        pattern_index = (pattern_index + 1) % len(pattern)

        # Check if the rock would hit anything by moving sideways.
        # If it does, don't move it
        if valid_rock(r_moved):
            r = r_moved

        # Move rock down
        r_moved = coords_set_move(r, 0, -1)
        if valid_rock(r_moved):
            r = r_moved
        else:
            # The rock hit something going down,
            # this is it's final resting position
            break

    # Add the new rock to the floor
    floor.update(r)

    # Compute new floor elevation
    for c in r:
        if c[1] > floor_highest:
            floor_highest = c[1]

# Part 1, just simulate falling rocks for 2022 iterations
rock_index = 0
floor = {(x,0) for x in range(7)}
floor_highest = 0
pattern_index = 0

for i in range(2022):
    fall_rock(rocks[rock_index])
    rock_index = (rock_index + 1) % len(rocks)
    
print(floor_highest)

# Part 2
# We can't run the simulation for 1000000000000 steps, this takes way too long.
# Instead, store the floor state and look for loops.

# If there is a full line somewhere in the floor, no rock can move below it.
# All information below this line is irrelevant and can be discarded.
def prune_floor():
    for h in range(floor_highest, -1, -1):
        test = {(x,h) for x in range(7)}
        if all([t in floor for t in test]):
            to_delete = {(x,hh) for x in range(7) for hh in range(h - 1, -1, -1)}
            floor.difference_update(to_delete)
            break

seen_states = dict()
# Stores current simulation state with index i.
# If this state was already seen, returns the index of
# the previously-seen state, and the repeating state
def seen_state(i):
    floor_state = coords_set_move(floor, 0, -floor_highest)
    if (rock_index, pattern_index) not in seen_states:
        seen_states[(rock_index, pattern_index)] = [(i, floor_highest, floor_state)]
    else:
        for st in seen_states[(rock_index, pattern_index)]:
            if st[2] == floor_state:
                return st
        else:
            seen_states[(rock_index, pattern_index)].append((i, floor_highest, floor_state))

    return None

rock_index = 0
floor = {(x,0) for x in range(7)}
floor_highest = 0
pattern_index = 0

for i in range(10000):
    prune_floor()

    loop_info = (i, seen_state(i))
    if loop_info[1] is not None:
        break

    fall_rock(rocks[rock_index])
    rock_index = (rock_index + 1) % len(rocks)
else:
    print('No loop found after 10000 iterations')
    exit(-1)

loop_length = loop_info[0] - loop_info[1][0]
loop_height_difference = floor_highest - loop_info[1][1]

N_remaining = 1000000000000 - i

# Now we know the loop length. Fast-forward the simulation.
count_easy_add = N_remaining // loop_length
floor = coords_set_move(floor, 0, loop_height_difference * count_easy_add)
floor_highest += loop_height_difference * count_easy_add
N_remaining -= count_easy_add * loop_length

# We stopped at the last loop before the end,
# run simulation for the remaining steps
while N_remaining > 0:
    fall_rock(rocks[rock_index])
    rock_index = (rock_index + 1) % len(rocks)
    N_remaining -= 1

print(floor_highest)
