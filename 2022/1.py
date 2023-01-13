#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

most = [0, 0, 0]
curr = 0

with open('1_input') as fd:
    for line in fd:
        try:
            curr = curr + int(line)
        except ValueError:
            if curr > most[0]:
                most[2] = most[1]
                most[1] = most[0]
                most[0] = curr
            elif curr > most[1]:
                most[2] = most[1]
                most[1] = curr
            elif curr > most[0]:
                most[0] = curr
            
            curr = 0

# Part 1
print(most[0])

# Part 2
print(sum(most))
