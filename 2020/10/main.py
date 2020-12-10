import collections
import sys

def num_routes(adapters):
    routes = collections.defaultdict(lambda: 0)
    routes[0] = 1  # the starting joltage
    for a in adapters[1:]:
        # The number of routes to an adapter is the sum of the number of routes
        # to all adapters which can reach the given adapter.
        routes[a] = sum([routes[a-x] for x in [1, 2, 3]])
    return max(routes.values())

def joltage_diffs(adapters):
    diffs = collections.defaultdict(lambda: 0)
    for i in range(len(adapters)):
        diffs[adapters[i] - adapters[i-1]] += 1
    return diffs


input_path = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_path, 'rt') as f:
    adapters = sorted([int(x) for x in f.readlines()])

adapters = [0] + adapters  # add 0 jolt outlet
adapters.append(adapters[-1] + 3)  # add device

# Part 1
diffs = joltage_diffs(adapters)
print(f'Part 1: {diffs[1] * diffs[3]}')

# Part 2
routes = num_routes(adapters)
print(f'Part 2: {routes}')
