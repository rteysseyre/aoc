#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

def is_correctly_ordered(left, right):
    if type(left) == int and type(right) == int:
        if left < right:
            return True
        if left > right:
            return False
        return None

    if type(left) == list and type(right) == type(None):
        return False

    if type(left) == type(None) and type(right) == list:
        return True

    if type(left) == list and type(right) == list:
        if len(left) == 0 and len(right) > 0:
            return True

        if len(left) > 0 and len(right) == 0:
            return False

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

total = 0
index = 1
with iter(open('13_input')) as lines:
    while True:
        try:
            left = eval(next(lines))
            right = eval(next(lines))

            val = is_correctly_ordered(left, right)
            assert(val is not None)
            if val:
                total += index

            index += 1
            next(lines)
        except StopIteration:
            break

print(total)
