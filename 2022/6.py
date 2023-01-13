#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

with open('6_input') as fd:
    data = fd.readlines()[0]

def all_chars_different(stuff):
    unique = []
    for c in stuff:
        if c in unique:
            return False
        unique.append(c)
    return True

def get_answer(marker_length):
    last_chars = []
    index = 0
    
    for c in data:
        index += 1
        last_chars.append(c)
        if len(last_chars) < marker_length:
            continue
    
        if len(last_chars) > marker_length:
            last_chars.pop(0)
    
        if all_chars_different(last_chars):
            break

    return index

print(get_answer(4))
print(get_answer(14))
