#!/usr/bin/env python3
# Raphaël Teysseyre, 2023

import re
import itertools

# Cube faces are numbered and oriented as such
# ^ symbol defines the "up" direction on the face
#
#             +-----+
#             | 0 ^ |
#             |     |
# +-----+-----+-----+-----+
# | 1 ^ | 2 ^ | 3 ^ | 4 ^ |
# |     |     |     |     |
# +-----+-----+-----+-----+
#             | 5 ^ |
#             |     |
#             +-----+
#

# Travel directions
RIGHT = 0
DOWN  = 1
LEFT  = 2
UP    = 3

INPUT_FILE = '22_input'

if INPUT_FILE == '22_input':
    # Manually define the cube map for the input file.
    # A more elegant solution would be to compute the folding
    # at run time. Sounds complicated.
    cube_map = (((1, '^'), (2, '^')),
                ((5, 'v'), ),
                ((4, 'v'), (3, 'v')),
                ((0, '<'),))

    # Cube face size for this file
    face_size = 50

    # Cursor coordinates are a tuple of (cube_face, x, y, direction)
    starting_coordinates = (1, 0, 0, RIGHT)
elif INPUT_FILE == '22_test_input':
    cube_map = (((0, '^'),),
                ((1, '^'), (2, '^'), (3, '^')),
                ((5, '^'), (4, '>')))

    face_size = 4
    starting_coordinates = (0, 0, 0, RIGHT)
else:
    print('Unknown input file, cube map is to be entered')
    exit(-1)

# This dictionary is indexed by face ID. Each element is
# a set containing the (x, y) coordinates of the walls
# on the face. (0, 0) is top-left, x positive to the right,
# y positive towards bottom
walls = dict()

# Given a (x,y) coordinate tuple, or a set of such coordinates,
# rotate 90° to the right around the center of the face.
# Apply several times to rotate more.
def rotate(coords):
    r = lambda c : (face_size - 1 - c[1], c[0])

    if isinstance(coords, tuple):
        return r(coords)
    else:
        return set(map(r, coords))

# Load up the input file
lines = [l.strip() for l in open(INPUT_FILE).readlines()]

# Read the path instructions
path = re.findall('\d+|[LR]', lines[-1])

# Read the cube map
for (imr, map_row) in enumerate(cube_map):
    for (imc, face) in enumerate(map_row):
        walls[face[0]] = set()
        for y, x in itertools.product(range(face_size), range(face_size)):
            if lines[imr * face_size + y][imc * face_size + x] == '#':
                walls[face[0]].add((x,y))

        # Reorient the face in our reference frame (all faces up)
        if face[1] == '>':
            walls[face[0]] = rotate(rotate(rotate(walls[face[0]])))
        elif face[1] == 'v':
            walls[face[0]] = rotate(rotate(walls[face[0]]))
        elif face[1] == '<':
            walls[face[0]] = rotate(walls[face[0]])

# Not used, can be used for visualisation. Kept here for posterity
def print_map(coords_history = set()):
    # Strip orientation information from coords history
    coords_history = set(map(lambda c : c[0:3], coords_history))

    def plot_faces(faces, offset):
        for r in range(face_size):
            str = ' ' * offset

            for f in faces:
                for c in range(face_size):
                    if (0, c, r) in coords_history: str += 'X'
                    elif (c, r) in walls[0]:        str += '#'
                    else:                           str += '-'

            print(str)

    plot_faces([0], 2 * face_size)
    plot_faces([1, 2, 3, 4], 0)
    plot_faces([5], 2 * face_size)

# If coordinates fall outside a face, move them to
# the correct location on the correct face.
def normalize(c):
    f, x, y, direction = c
    if x >= 0 and x < face_size and y >= 0 and y < face_size:
        return c

    if x < 0: # Dropped to the left of a face
        return ((2, y, 0, DOWN),
                (4, face_size - 1, y, LEFT),
                (1, face_size - 1, y, LEFT),
                (2, face_size - 1, y, LEFT),
                (3, face_size - 1, y, LEFT),
                (2, face_size - 1 - y, face_size - 1, UP))[f]
    elif x >= face_size: # Dropped to the right of a face
        return ((4, face_size - 1 - y, 0, DOWN),
                (2, 0, y, RIGHT),
                (3, 0, y, RIGHT),
                (4, 0, y, RIGHT),
                (1, 0, y, RIGHT),
                (4, y, face_size - 1, UP))[f]
    elif y < 0: # Dropped to the top of a face
        return ((1, face_size - 1 - x, 0, DOWN),
                (0, face_size - 1 - x, 0, DOWN),
                (0, 0, x, RIGHT),
                (0, x, face_size - 1, UP),
                (0, face_size - 1, face_size - 1 - x, LEFT),
                (3, x, face_size - 1, UP))[f]
    else: # Dropped to the bottom of a face
        return ((3, x, 0, DOWN),
                (5, face_size - 1 - x, face_size - 1, UP),
                (5, 0, face_size - 1 - x, RIGHT),
                (5, x, 0, DOWN),
                (5, face_size - 1, x, LEFT),
                (1, face_size - 1 - x, face_size - 1, UP))[f]

# Move the cursor one step forward
def advance(c):
    if   c[3] == RIGHT: return normalize((c[0], c[1] + 1, c[2]    , RIGHT))
    elif c[3] == DOWN:  return normalize((c[0], c[1]    , c[2] + 1, DOWN ))
    elif c[3] == LEFT:  return normalize((c[0], c[1] - 1, c[2]    , LEFT ))
    else:               return normalize((c[0], c[1]    , c[2] - 1, UP   ))

# Rotate the cursor
def turn_left(c):
    return c[0:3] + ((c[3] - 1) % 4,)

def turn_right(c):
    return c[0:3] + ((c[3] + 1) % 4,)

# Check if there is a wall at a coordinates point
def is_wall(c):
    return (c[1], c[2]) in walls[c[0]]

# Follow the path
pos = starting_coordinates
for p in path:
    if   p == 'L': pos = turn_left(pos)
    elif p == 'R': pos = turn_right(pos)
    else: # Advance p step
        for _ in range(int(p)):
            test = advance(pos)
            if is_wall(test):
                break
            pos = test

# Convert back to original-map coordinates
for (imr, map_row) in enumerate(cube_map):
    for (imc, face) in enumerate(map_row):
        if face[0] == pos[0]:
            if face[1] == '>':
                # Face was rotated to the left, we need to
                # rotate our result to the right to go back
                # to original-map coordinates
                x, y = rotate(pos[1:3])
                direction = (pos[3] + 1) % 4
            elif face[1] == 'v':
                x, y = rotate(rotate(pos[1:3]))
                direction = (pos[3] + 2) % 4
            elif face[1] == '<':
                x, y = rotate(rotate(rotate(pos[1:3])))
                direction = (pos[3] + 3) % 4
            else:
                x, y = pos[1:3]
                direction = pos[3]

            # x/y are indexed from zero,
            # row/columns are indexed from 1
            row = y + 1 + imr * face_size
            col = x + 1 + imc * face_size

            # Print answer, done.
            print(1000 * row + 4 * col + direction)
            exit(0)
