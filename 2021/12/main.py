from collections import defaultdict
import fileinput

def explore(node, cave, visited, lower_revisited=False):
    # Whether or not a lower case node has already been revisisted
    # IE whether or not we can revisit a lowercase tile
    lower_revisited = lower_revisited or (node in visited)
    if node.islower(): visited.add(node)

    if lower_revisited:
        valid_neighbors = filter(lambda n: n not in visited and n != 'start', cave[node])
    else:
        valid_neighbors = filter(lambda n: n != 'start', cave[node])
        
    routes = 0
    for n in valid_neighbors:
        if n == 'end':
            routes += 1
        else:
            routes += explore(n, cave, visited.copy(), lower_revisited)
    return routes

# Parse input
cave = defaultdict(list)
for line in map(lambda x: x.strip(), fileinput.input()):
    src, dst = line.split('-')
    cave[src].append(dst)
    cave[dst].append(src)

# Part 1
routes = explore('start', cave, set(), True)
print(routes)    

# Part 2
routes = explore('start', cave, set())
print(routes)    
