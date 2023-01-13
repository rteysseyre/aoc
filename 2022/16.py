#!/usr/bin/env python3
# Raphaël Teysseyre, 2023

# I used help from reddit for this one, for computing the distance between
# all valves (Floyd-Warshall), and for the bitmask trick at the end that
# speeds up the comparison between two paths.

FILENAME = '16_input'

# Returns (valve name, flow rate, connected to).
def read_valves(filename):
    for line in open(filename):
        words = line.strip().split()
        yield (words[1], int(words[4][5:-1]), [w[0:2] for w in words[9:]])

graph = { valve : con for valve, flow, con in read_valves(FILENAME) }
flows = { valve : flow for valve, flow, con in read_valves(FILENAME) }
distances = {(v1, v2) : 1 if v2 in graph[v1] else 1000 for v1 in graph for v2 in graph }

# Compute minimum distance between all valves using Floyd-Warshall algorithm
for k in graph:
    for j in graph:
        for i in graph:
            distances[i, j] = min(distances[i, j], distances[i, k] + distances[k, j])

# Prune zero-flow valves
for v1 in graph:
    if v1 == 'AA':
        continue

    for v2 in graph:
        if flows[v1] == 0 or flows[v2] == 0 or v1 == v2:
            del distances[v1, v2]

to_prune = []
for v, f in flows.items():
    if f == 0:
        to_prune.append(v)

for p in to_prune:
    del graph[p]
    del flows[p]

# Assign a unique bit to each valve
valve_ids = { valve : 1 << i for i, valve in enumerate(graph) }

def get_bitmask(path):
    out = 0
    for v in path:
        out |= valve_ids[v]
    return out

def visit(node, opened, current_total, time_remaining):
    global best_total
    global possible_paths

    if time_remaining <= 0:
        return

    if current_total > best_total:
        best_total = current_total

    possible_paths.append((get_bitmask(opened), current_total))

    for v in graph:
        if v in opened:            
            continue

        visit(v, opened + [v],
              current_total + flows[v] * (time_remaining - distances[node, v] - 1),
              time_remaining - distances[node, v] - 1)

# Part 1: 30 steps search     
best_total = 0
possible_paths = []   
visit('AA', [], 0, 30)
print(best_total)

# Part 2: 26 steps search, combine best 2 paths
best_total = 0
possible_paths = []
visit('AA', [], 0, 26)

best_total = 0
for (i, p1) in enumerate(possible_paths):
    if i % 2000 == 0:
        print(f'{i/len(possible_paths)*100:.1f} % processed')

    for p2 in possible_paths[i+1:]:
        # If p1 and p2 both open the same valve, time was wasted
        # and there exist a better solution where either p1 or p2
        # has skipped this valve. In this case computing p1[1] + p2[1]
        # is wrong because it would count the flow of the double-opened
        # valve twice
        if p1[0] & p2[0]:
            continue
        elif p1[1] + p2[1] > best_total:
            best_total = p1[1] + p2[1]

print(best_total)
