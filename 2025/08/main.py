import lib.aoc as aoc

from itertools import combinations
from math import prod, sqrt

circuit_sizes = {}


class Junction:
    def __init__(self, x, y, z, circuit):
        self.x = x
        self.y = y
        self.z = z
        self.circuit = circuit
        self.connections = []
        circuit_sizes[circuit] = 1

    def connect(self, other: "Junction"):
        self.connections.append(other)
        other.connections.append(self)
        other.update_circuit(self.circuit)

    def update_circuit(self, new_circuit):
        """Propogate new circuit id via DFS"""
        if self.circuit == new_circuit:
            return

        circuit_sizes[self.circuit] -= 1
        if circuit_sizes[self.circuit] == 0:
            del circuit_sizes[self.circuit]
        circuit_sizes[new_circuit] += 1

        self.circuit = new_circuit
        for connection in self.connections:
            connection.update_circuit(new_circuit)


def dist(a: Junction, b: Junction):
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


# Parse input
junctions = []
for i, line in enumerate(aoc.input_lines()):
    x, y, z = [int(x) for x in line.split(",")]
    junctions.append(Junction(x, y, z, i))

# Pre-calculate all pairwise distances
edges = []
for a, b in combinations(junctions, 2):
    edges.append((dist(a, b), a, b))

# Make the connections!
connections = 0
for dist, a, b in sorted(edges):
    if connections == 1000:
        # Part 1, product of 3 largest circuits
        aoc.output(prod(sorted(circuit_sizes.values(), reverse=True)[:3]))
    connections += 1
    if a.circuit == b.circuit:
        continue  # already connected

    a.connect(b)
    if len(circuit_sizes) == 1:
        # Part 2
        aoc.output(a.x * b.x)
        break
