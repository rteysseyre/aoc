#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

elevations = []
visited = []

for line in open('12_input'):
    curr_line = []
    for c in line:
        if c == 'S':
            start_position = [len(elevations), len(curr_line)]
            curr_line.append(0)
            continue

        if c == 'E':
            end_position = [len(elevations), len(curr_line)]
            curr_line.append(ord('z') - ord('a'))
            continue

        curr_line.append(ord(c) - ord('a'))

    elevations.append(curr_line)

def get_value(pos, matrix):
    return matrix[pos[0]][pos[1]]

def set_value(pos, matrix, val):
    matrix[pos[0]][pos[1]] = val

def get_elevation(pos):
    return get_value(pos, elevations)

def is_visited(pos):
    return get_value(pos, visited)

def set_visited(pos):
    return set_value(pos, visited, True)

def is_valid_pos(pos):
    return (pos[0] >= 0
            and pos[1] >= 0
            and pos[0] < len(elevations)
            and pos[1] < len(elevations[0]))

def get_new_positions(pos):
    new_pos = [
        [pos[0] - 1, pos[1]],
        [pos[0] + 1, pos[1]],
        [pos[0], pos[1] - 1],
        [pos[0], pos[1] + 1]]
    return [p for p in new_pos if is_valid_pos(p)]

MAX_STEPS = 500

def get_step_counts(start_position):
    global visited

    visited = [[False for _ in elevations[0]] for _ in elevations]
    front_line = [start_position]
    step_count = 0

    while not is_visited(end_position):
        new_front_line = []

        for p in front_line:
            for pp in get_new_positions(p):
                if is_visited(pp):
                    continue

                if get_elevation(pp) <= get_elevation(p) + 1:
                    new_front_line.append(pp)
                    set_visited(pp)

        step_count += 1
        front_line = new_front_line

        if step_count > MAX_STEPS:
            break

    return step_count

# Part 1
print(get_step_counts(start_position))

# Part 2
# Try from all places with elevation = 0.
# Starting from the end until finding a place with elevation = 0
# would be more elegant (and probably faster), but this would
# mean more code change. This is fast enough and gives the correct answer.
min_steps = MAX_STEPS
for x in range(len(elevations)):
    for y in range(len(elevations[0])):
        if get_elevation([x, y]) == 0:
            st = get_step_counts([x, y])
            if st < min_steps:
                min_steps = st

print(min_steps)
