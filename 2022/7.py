#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

class Node:
    TYPE_UNDEFINED = 0
    TYPE_FOLDER = 1
    TYPE_FILE = 2

    def __init__(self, name = '', type = TYPE_UNDEFINED, size = 0):
        self.name = name
        self.parent = None
        self.children = []
        self.size = size
        self.type = type

    def _validType(func):
        def wrapper(self, *args, **kwargs):
            if self.type != Node.TYPE_FILE and self.type != Node.TYPE_FOLDER:
                raise ValueError('Invalid Node type, must be file or folder')
            return func(self, *args, **kwargs)
        return wrapper

    def _folderType(func):
        def wrapper(self, *args, **kwargs):
            if self.type != Node.TYPE_FOLDER:
                raise ValueError('Invalid Node type, must be folder')
            return func(self, *args, **kwargs)
        return wrapper

    def getParent(self):
        return self.parent

    @_folderType
    def getChild(self, name):
        for c in self.children:
            if c.name == name:
                return c
        raise ValueError('Child not found: ' + name)

    @_folderType
    def addChild(self, n):
        n.parent = self
        self.children.append(n)

    @_validType
    def getSize(self):
        if self.type == Node.TYPE_FILE:
            return self.size

        if self.type == Node.TYPE_FOLDER:
            return sum([x.getSize() for x in self.children])

    @_validType
    def __str__(self, prefix = ''):
        if self.type == Node.TYPE_FILE:
            return prefix + self.name + ' ' + str(self.getSize())

        if self.type == Node.TYPE_FOLDER:
            ret = prefix + self.name + '/ ' + str(self.getSize())
            for c in self.children:
                ret += '\n' + c.__str__(prefix + '  ')
            return ret

root = Node(type = Node.TYPE_FOLDER)
currNode = root

with iter(open('7_input')) as lineReader:
    try:
        line = next(lineReader)
        while True:
            if line.startswith('$ cd'):
                if line.startswith('$ cd /'):
                    currNode = root
                elif line.startswith('$ cd ..'):
                    currNode = currNode.getParent()
                else:
                    currNode = currNode.getChild(line[5:-1])
                line = next(lineReader)

            elif line.startswith('$ ls'):
                while True:
                    line = next(lineReader)
                    if line.startswith('$'):
                        break

                    if line.startswith('dir'):
                        currNode.addChild(Node(type = Node.TYPE_FOLDER,
                                               name = line[4:-1]))
                    else:
                        tokens = line.split()
                        currNode.addChild(Node(type = Node.TYPE_FILE,
                                               name = tokens[1],
                                               size = int(tokens[0])))

            else:
                raise ValueError('Failed to parse line: ' + line)

    except StopIteration:
        pass

# Part 1
def step1(node):
    count = 0
    if node.type == Node.TYPE_FOLDER:
        if node.getSize() <= 100000:
            count += node.getSize()
        for c in node.children:
            count += step1(c)
    return count

print(step1(root))

# Part 2
TOTAL_SPACE = 70000000
REQUIRED_SPACE = 30000000
FREE_SPACE = TOTAL_SPACE - root.getSize()
MIN_DELETE = REQUIRED_SPACE - FREE_SPACE

def step2(node, min_delete, best_candidate):
    if node.type == Node.TYPE_FOLDER:
        if node.getSize() > min_delete:
            if node.getSize() < best_candidate.getSize():
                best_candidate = node
        for c in node.children:
            best_candidate = step2(c, min_delete, best_candidate)
    return best_candidate

print(step2(root, MIN_DELETE, root).getSize())
