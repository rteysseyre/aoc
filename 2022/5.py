#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

class Stacks:
    def __init__(self, fd = None):
        self.content = []
        if fd is None:
            return

        fd.seek(0)
        # box content are at characters 1, 5, 9, ... of each line
        def get_box_content(line, id):
            c = line[1 + id * 4]
            if c.isspace():
                return None
            return c

        for line in fd:
            if line[0] != '[':
                break

            index = 0
            while True:
                try:
                    c = get_box_content(line, index)
                except IndexError:
                    # Tried to read past end of line
                    break

                if index >= len(self.content):
                    self.content.append([])

                if c is not None:
                    self.content[index].append(c)

                index += 1

        # We read the piles from top to bottom,
        # reverse all piles to have the bottom at
        # index 0.
        for s in self.content:
            s.reverse()

    # Move crates one at a time
    def move_9000(self, fro, to, count):
        self.content[to].append(self.content[fro].pop())
        if count > 1:
            self.move_9000(fro, to, count - 1)

    # Move all crates at once
    def move_9001(self, fro, to, count):
        self.content[to] += self.content[fro][-count:]
        self.content[fro] = self.content[fro][0:-count]

    def __str__(self):
        return str(self.content)

    def get_top_signature(self):
        str = ''
        for s in self.content:
            if len(s) > 0:
                str += s[-1]
        return str

with open('5_input') as fd:
    st1 = Stacks(fd)
    st2 = Stacks(fd)

for line in open('5_input'):
    if line[0:4] != 'move':
        continue

    tokens = line.split(' ')

    st1.move_9000(int(tokens[3]) - 1, int(tokens[5]) - 1, int(tokens[1]))
    st2.move_9001(int(tokens[3]) - 1, int(tokens[5]) - 1, int(tokens[1]))

print(st1.get_top_signature())
print(st2.get_top_signature())
