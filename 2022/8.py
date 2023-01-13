#!/usr/bin/env python3
# Raphaël Teysseyre, 2022

treeGrid = []
for line in open('8_input'):
    treeGrid.append([int(x) for x in line[:-1]])

def getRow(i):
    return treeGrid[i]

def getCol(i):
    return [treeGrid[y][i] for y in range(len(treeGrid))]

def edgeTree(x, y):
    return x == 0 or y == 0 or x == len(line) - 1 or y == len(line[0]) - 1
    
# Part 1
visibleCount = 0
for y in range(len(treeGrid)):
    for x in range(len(treeGrid[0])):
        if edgeTree(x, y):
            visibleCount += 1
            continue

        thisHeight = treeGrid[y][x]
        
        if (   all([h < thisHeight for h in getRow(y)[:x]])
            or all([h < thisHeight for h in getRow(y)[x+1:]])
            or all([h < thisHeight for h in getCol(x)[:y]])
            or all([h < thisHeight for h in getCol(x)[y+1:]])):
            visibleCount += 1

print(visibleCount)

# Part 2
def getPartialScore(thisHeight, lst):
    s = 0
    for h in lst:
        s += 1
        if h >= thisHeight:
            break
    return s
        
bestScenicScore = 0
for y in range(len(treeGrid)):
    for x in range(len(treeGrid[0])):
        if edgeTree(x, y):
            continue

        thisHeight = treeGrid[y][x]
        scenicScore = (
              getPartialScore(thisHeight, reversed(getRow(y)[:x]))
            * getPartialScore(thisHeight, getRow(y)[x+1:])
            * getPartialScore(thisHeight, reversed(getCol(x)[:y]))
            * getPartialScore(thisHeight, getCol(x)[y+1:]))
        
        if scenicScore > bestScenicScore:
            bestScenicScore = scenicScore

print(bestScenicScore)
 
