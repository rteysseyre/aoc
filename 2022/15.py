#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

def manhattan_distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

class Span:
    def __init__(self, start, end):
        assert(start <= end)
        self.start = start
        self.end = end

    def contains(self, other):
        # Special case if other is a scalar
        if type(other) is int or type(other) is float:
            return other >= self.start and other <= self.end

        # Default case: expect a span-like argument
        return self.start <= other.start and self.end >= other.end

    def intersects(self, other):
        return (self.contains(other)
                or other.contains(self)
                or self.contains(other.start)
                or self.contains(other.end))

    def union(self, other):
        if not self.intersects(other):
            raise ValueError('Argument does not insersects self.')

        return Span(min(self.start, other.start), max(self.end, other.end))

    @property
    def length(self):
        return self.end - self.start + 1

    def __repr__(self):
        return '(' + str(self.start) + ', ' + str(self.end) + ')'

class Sensor:
    def __init__(self, txt):
        words = txt.strip().split()
        self.x = int(words[2][2:-1])
        self.y = int(words[3][2:-1])
        self.bx = int(words[8][2:-1])
        self.by = int(words[9][2:])

    @property
    def bdist(self):
        return manhattan_distance(self.x, self.y, self.bx, self.by)

    def getXSpan(self, y):
        if abs(y - self.y) > self.bdist:
            return None

        return Span(self.x - (self.bdist - abs(y - self.y)),
                    self.x + (self.bdist - abs(y - self.y)))

    def __repr__(self):
        return f'Sensor at x={self.x}, y={self.y}: closest beacon is at x={self.bx}, y={self.by}'

class SpanList:
    def __init__(self, lst = None):
        self.spans = []
        if lst is not None:
            for elt in lst:
                self.append(elt)

    def append(self, s):
        if s is None:
            return

        if len(self.spans) == 0:
            self.spans = [s]

        newSpans = []
        for x in self.spans:
            if s.intersects(x):
                s = s.union(x)
            else:
                 newSpans.append(x)

        newSpans.append(s)
        self.spans = newSpans

    def __len__(self):
        return len(self.spans)

    def __repr__(self):
        return str(self.spans)

# Part 1
sensors = [Sensor(l) for l in open('15_input')]
sl = SpanList([s.getXSpan(2000000) for s in sensors])
print(sl.spans[0].end - sl.spans[0].start)

# Part 2
# A bit slow, but faster than optimizing the code
for y in range(4000000):
    if y % 40000 == 0:
        print(f'Processed {y/4000000*100:.0f} % of lines')

    sl = SpanList([s.getXSpan(y) for s in sensors])
    if len(sl) > 1:
        lst = sorted([sl.spans[0].start, sl.spans[0].end, sl.spans[1].start, sl.spans[1].end])
        assert lst[2] - lst[1] == 2
        print(4000000 * (lst[1] + 1) + y)
        break
