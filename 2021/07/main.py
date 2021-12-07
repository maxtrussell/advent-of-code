""" Could be optimized and cleaned up, but no time today :) """

import collections
import fileinput

crab_pos = collections.Counter(map(int, next(fileinput.input()).split(',')))
costs = {}
for dst in crab_pos:
    costs[dst] = 0
    for src, count in crab_pos.items():
        costs[dst] += abs(dst - src) * count
print(min(costs.values()))

costs = {}
for dst in range(max(crab_pos.keys())):
    costs[dst] = 0
    for src, count in crab_pos.items():
        delta = abs(dst - src)
        fuel = sum(range(1, delta+1))
        costs[dst] += fuel * count
print(min(costs.values()))
