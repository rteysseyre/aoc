#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

from functools import cmp_to_key

def is_correctly_ordered(left, right):
    if type(left) == int and type(right) == int:
        if left < right:
            return 1
        if left > right:
            return -1
        return None

    if type(left) == list and type(right) == type(None):
        return -1

    if type(left) == type(None) and type(right) == list:
        return 1

    if type(left) == list and type(right) == list:
        if len(left) == 0 and len(right) > 0:
            return 1

        if len(left) > 0 and len(right) == 0:
            return -1

        if len(left) == 0 and len(right) == 0:
            return None
        
        car_val = is_correctly_ordered(left[0], right[0])
        if car_val is None:
            return is_correctly_ordered(left[1:], right[1:])
        else:
            return car_val

    if type(left) == int and type(right) == list:
        return is_correctly_ordered([left], right)

    if type(left) == list and type(right) == int:
        return is_correctly_ordered(left, [right])

    # We should have processed all cases
    assert(False)

data = []
for l in open('13_input'):
    if l.startswith('['):
        data.append(eval(l))

data.append([[2]])
data.append([[6]])

data.sort(key = cmp_to_key(is_correctly_ordered), reverse=True)

answer = 1
for i in range(len(data)):
    if data[i] == [[2]] or data[i] == [[6]]:
        answer *= i + 1

print(answer)
