import lib.aoc as aoc

from collections import Counter

left, right = [], []
for line in aoc.input_lines():
    l, r = line.split("   ")
    left.append(int(l))
    right.append(int(r))

counts = Counter(right)

p1, p2 = 0, 0
for l, r in zip(sorted(left), sorted(right)):
    p1 += abs(l - r)
    p2 += l * counts[l]

aoc.output(p1)
aoc.output(p2)
