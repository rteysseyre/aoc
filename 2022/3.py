#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

def get_priority(char):
    code = ord(char)
    if code < ord('a'): # Uppercase
        return code - ord('A') + 27
    else: # Lowercase
        return code - ord('a') + 1

# Part 1
total = 0
for line in open('3_input'):
   left  = set(line[:(len(line) - 1)//2])
   right = set(line[(len(line) - 1)//2:-1])

   common = set.intersection(left, right)

   assert len(common) == 1
   total += get_priority(common.pop())

print(total)    

# Part 2
total = 0
with open('3_input') as fd:
    try:
        while True:
            handle = iter(fd)

            elf1 = set(next(fd)[:-1])
            elf2 = set(next(fd)[:-1])
            elf3 = set(next(fd)[:-1])

            common = set.intersection(elf1, elf2, elf3)

            assert len(common) == 1
            total += get_priority(common.pop())
    except StopIteration:
        pass

print(total)
