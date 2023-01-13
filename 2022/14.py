#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

rockLines=[]
for l in open('14_input'):
    data = l.split(' -> ')
    rockLines.append([])
    for d in data:
        rockLines[-1].append([int(a) for a in d.split(',')])

rockContent={}
for l in rockLines:
    for i in range(len(l) - 1):
        start = l[i].copy()
        end = l[i+1].copy()

        while start != end:
            rockContent[tuple(start)] = True
            if start[0] == end[0]:
                if start[1] < end[1]:
                    start[1] += 1
                else:
                    start[1] -= 1
            else:
                if start[0] < end[0]:
                    start[0] += 1
                else:
                    start[0] -= 1

        rockContent[tuple(end)] = True

maxDepth = max([x[1] for x in rockContent]) + 1

class SandCantMove(Exception):
    pass

def getSandCount(hasFloor):
    sandContent = {}

    def getNewSandPosition(pos):
        tentativePositions = [
            (pos[0], pos[1] + 1),
            (pos[0] - 1, pos[1] + 1),
            (pos[0] + 1, pos[1] + 1)]
    
        for p in tentativePositions:
            if p not in rockContent and p not in sandContent:
                return p
    
        raise SandCantMove()

    sandCount = 0
    while True:
        sandPosition = [500, 0]
        try:
            while True:
                sandPosition = getNewSandPosition(sandPosition)
                if sandPosition[1] == maxDepth:
                    if hasFloor:
                        raise SandCantMove()
                    else:
                        return sandCount
        except SandCantMove:
            sandContent[tuple(sandPosition)] = True
            sandCount += 1
    
        if sandPosition == [500, 0]:
            break

    return sandCount

print(getSandCount(False))
print(getSandCount(True))
