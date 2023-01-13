#!/usr/bin/env python3
# Raphaël Teysseyre, 2023

def mix(lst):
    for k in range(len(lst)):
        i = 0
        while lst[i][1] != k:
            i += 1

        # Be careful: going from the end of the list to
        # the beginning of the list is not actually a move,
        # because this is a circular buffer
        new_index = i + lst[i][0] % (len(lst) - 1)
        if new_index >= len(lst):
            new_index = new_index - len(lst) + 1

        if new_index < i:
            lst = lst[:new_index] + [lst[i]] + lst[new_index:i] + lst[i+1:]
            i += 1
        elif new_index > i:
            lst = lst[:i] + lst[i+1:new_index + 1] + [lst[i]] + lst[new_index + 1:]
        else:
            i += 1

    return lst

lst = [[int(a), i] for i, a in enumerate(open('20_input'))]

def get_result(lst):
    for i, e in enumerate(lst):
        if e[0] != 0:
            continue

        return (lst[(i + 1000) % len(lst)][0]
                + lst[(i + 2000) % len(lst)][0]
                + lst[(i + 3000) % len(lst)][0])

# Part 1
print(get_result(mix(lst)))

# Part 2
for e in lst:
    e[0] *= 811589153

for i in range(10):
    lst = mix(lst)
print(get_result(lst))
