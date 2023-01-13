#!/usr/bin/env python3
# Raphaël Teysseyre, 2023

total_exposed = 0
current_cubes = []

def get_adjacent(coords):
    return ((coords[0], coords[1], coords[2] - 1),
            (coords[0], coords[1], coords[2] + 1),
            (coords[0], coords[1] - 1, coords[2]),
            (coords[0], coords[1] + 1, coords[2]),
            (coords[0] - 1, coords[1], coords[2]),
            (coords[0] + 1, coords[1], coords[2]))

# Part 1: read cubes, compute total number
# of faces that are exposed
for line in open('18_input'):
    coords = tuple(int(x) for x in line.strip().split(','))
    current_cubes.append(coords)
    total_exposed += 6
    for a in get_adjacent(coords):
        if a in current_cubes:
            # The new cube shares a face with a current cube.
            # remove those two faces from the exposed count
            total_exposed -= 2

print(total_exposed)

# Part 2
# Fill the space surrounding the shape to find the outside frontier

# Compute bounding box
bb_xmin = current_cubes[0][0]
bb_xmax = current_cubes[0][0]

bb_ymin = current_cubes[0][1]
bb_ymax = current_cubes[0][1]

bb_zmin = current_cubes[0][2]
bb_zmax = current_cubes[0][2]

for c in current_cubes:
    if c[0] < bb_xmin:
        bb_xmin = c[0]
    if c[0] > bb_xmax:
        bb_xmax = c[0]

    if c[1] < bb_ymin:
        bb_ymin = c[1]
    if c[1] > bb_ymax:
        bb_ymax = c[1]

    if c[2] < bb_zmin:
        bb_zmin = c[2]
    if c[2] > bb_zmax:
        bb_zmax = c[2]

# Grow the bounding box by one unit. This way we are sure that
# there is at least 1 free cube on all sides of the shape
bb_xmin -= 1
bb_xmax += 1
bb_ymin -= 1
bb_ymax += 1
bb_zmin -= 1
bb_zmax += 1

def in_bb(cube):
    return (cube[0] >= bb_xmin
            and cube[0] <= bb_xmax
            and cube[1] >= bb_ymin
            and cube[1] <= bb_ymax
            and cube[2] >= bb_zmin
            and cube[2] <= bb_zmax)

# Start painting the outside space from a corner of the bounding box
painted = [(bb_xmin, bb_ymin, bb_zmin)]
i = 0
total_exposed = 0

while i < len(painted):
    test = get_adjacent(painted[i])
    for t in test:
        if not in_bb(t) or t in painted:
            continue
        
        if t in current_cubes:
            total_exposed += 1
        else:
            painted.append(t)

    i += 1

print(total_exposed)
