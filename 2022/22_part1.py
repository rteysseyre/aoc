#!/usr/bin/env python3
# Raphaël Teysseyre, 2023

import re

lines = open('22_input').readlines()

m = [[x for x in l[:-1]] for l in lines[:-2]]
path = re.findall('\d+|[LR]', lines[-1])

def get_increment(direction):
    return [[1, 0], [0, 1], [-1, 0], [0, -1]][direction]

def get_val(pos):
    if pos[0] < 0 or pos[1] < 0:
        return ' '

    try:
        return m[pos[1]][pos[0]]
    except:
        return ' '

def move(pos, increment):
    new_pos = [pos[0] + increment[0], pos[1] + increment[1]]

    if get_val(new_pos) == ' ': # loop around
        if increment == [1, 0]:
            new_pos = [0, pos[1]]
            while get_val(new_pos) == ' ':
                new_pos[0] += 1
        elif increment == [-1, 0]:
            new_pos = [1000, pos[1]]
            while get_val(new_pos) == ' ':
                new_pos[0] -= 1
        elif increment == [0, 1]:
            new_pos = [pos[0], 0]
            while get_val(new_pos) == ' ':
                new_pos[1] += 1
        elif increment == [0, -1]:
            new_pos = [pos[0], 1000]
            while get_val(new_pos) == ' ':
                new_pos[1] -= 1

    if get_val(new_pos) == '.':
        return new_pos
    elif get_val(new_pos) == '#':
        return pos
    else:
        raise ValueError(new_pos)

# 0 -> right, 1 -> down, 2 -> left, 3 -> up
direction = 0
pos = [0, 0] # [X, Y] or [Column, row]

while get_val(pos) == ' ':
    pos[0] += 1

for instr in path:
    try:
        count = int(instr)
    except:
        if instr == 'R':
            direction += 1
        else:
            direction -= 1
        direction %= 4
    else:
        incr = get_increment(direction)
        for i in range(count):
            pos = move(pos, incr)

print((pos[1] + 1) * 1000 + (pos[0] + 1) * 4 + direction)
