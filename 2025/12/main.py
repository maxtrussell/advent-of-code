import lib.aoc as aoc

from math import prod

chunks = aoc.input_chunks()

# Calculate the minimum area each present takes up.
presents = []
for present in chunks[:-1]:
    presents.append(present.count("#"))

# Calculate how many bins could possibly hold their prescribed presents.
p1 = 0
for line in (l for l in chunks[-1].split("\n") if l):
    bin_size = prod(int(x) for x in line.split(":")[0].split("x"))
    num_presents = [int(x) for x in line.split(":")[1].split()]
    p1 += bin_size > sum(presents[i] * n for i, n in enumerate(num_presents))

aoc.output(p1)
