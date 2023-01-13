#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, other):
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other):
        return ((self.start >= other.start and
                 self.start <= other.end) or
                (self.end >= other.start and
                 self.end <= other.end) or
                self.contains(other) or
                other.contains(self))

    def __str__(self):
        return str(self.start) + ' - ' + str(self.end)

    @staticmethod
    def from_str(arg):
        l, r = arg.split('-')
        return Range(int(l), int(r))

total1 = 0
total2 = 0

for line in open('4_input'):
    r1, r2 = [Range.from_str(x) for x in line.split(',')]
    if r1.contains(r2) or r2.contains(r1):
        total1 += 1
    if r1.overlaps(r2):
        total2 += 1

print(total1)
print(total2)
    
