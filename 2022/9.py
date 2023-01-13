#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

def isCloseEnough(front, back):
    xDist = abs(front[0] - back[0])
    yDist = abs(front[1] - back[1])
    return xDist <= 1 and yDist <= 1

def sign(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1

def updatePosition(front, back):
    xSign = sign(front[0] - back[0])
    ySign = sign(front[1] - back[1])

    back[0] += xSign
    back[1] += ySign

DIRECTIONS = {
    'R': [1, 0],
    'U': [0, 1],
    'L': [-1, 0],
    'D': [0, -1]
}

def run(snakeLength):
    pos = [[0,0] for _ in range(snakeLength)]
    visitedPositions = [pos[-1].copy()]

    for line in open('9_input'):
        dir = DIRECTIONS[line[0]]
        count = int(line[2:])
    
        while count > 0:
            pos[0][0] += dir[0]
            pos[0][1] += dir[1]
    
            for (f, b) in zip(pos[:-1], pos[1:]):
                if not isCloseEnough(f, b):
                    updatePosition(f, b)
    
            if pos[-1] not in visitedPositions:
                    visitedPositions.append(pos[-1].copy())
    
            count -= 1

    return len(visitedPositions)

print(run(2))
print(run(10))
