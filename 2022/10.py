#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

# At the end of zeroth cycle, x = 1
x_value = [1]
px = 0

def plot():
    global px

    if (   x_value[-1] == px - 1
        or x_value[-1] == px
        or x_value[-1] == px + 1):
        print('#', end = '')
    else:
        print('.', end = '')

    px += 1
    if px > 39:
        print('')
        px = 0

def noop():
    plot()
    x_value.append(x_value[-1])

def addx(val):
    plot()
    x_value.append(x_value[-1])
    plot()
    x_value.append(x_value[-1] + val)

print('Part 2 answer:')
for line in open('10_input'):
    if line.startswith('noop'):
        noop()
    if line.startswith('addx'):
        addx(int(line.split(' ')[1]))

print('')

# We want the "signal strength" at those cycles
cycles = [20, 60, 100, 140, 180, 220]
total = 0
for c in cycles:
    total += c * x_value[c - 1]

print('Part 1 answer:')
print(total)
