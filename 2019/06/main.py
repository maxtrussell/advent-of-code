from collections import defaultdict

def make_graphs(input_):
    digraph = defaultdict(set)
    ugraph = defaultdict(set)
    for line in input_:
        orbitee, orbiter = line.split(')')
        digraph[orbitee].add(orbiter)
        ugraph[orbitee].add(orbiter)
        ugraph[orbiter].add(orbitee)
    return digraph, ugraph

def count_orbits(node, digraph, depth):
    orbits = 0
    for child in digraph[node]:
        orbits += depth + count_orbits(child, digraph, depth + 1)
    return orbits

def orbital_transfers(node, ugraph, seen):
    # breadth first search
    for neighbor in ugraph[node] - seen:
        seen.add(neighbor)
        if neighbor == 'SAN':
            return 0
        transfers = orbital_transfers(neighbor, ugraph, seen)
        if transfers is not None:
            return transfers + 1
    return None
        

with open('input.txt') as f:
    input_ = [l.strip() for l in f.readlines()]

digraph, ugraph = make_graphs(input_)
print(count_orbits('COM', digraph, 1))
print(orbital_transfers('YOU', ugraph, {'YOU'}) - 1)
