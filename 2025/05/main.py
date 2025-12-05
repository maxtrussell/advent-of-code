import lib.aoc as aoc


def merge(ranges):
    i = 0
    while i < len(ranges) - 1:
        a, b = ranges[i], ranges[i + 1]
        if a[1] >= b[0]:
            ranges[i] = [a[0], max(a[1], b[1])]
            del ranges[i + 1]
        else:
            i += 1
    return ranges


# Parse input
fresh, available = [], []
for line in aoc.input_lines():
    if not line:
        continue
    if "-" in line:
        fresh.append(list(int(x) for x in line.split("-")))
    else:
        available.append(int(line))

# Merge the ranges
fresh = merge(sorted(fresh))

p1 = 0
for ingredient in available:
    for a, b in fresh:
        if a <= ingredient <= b:
            p1 += 1
            break

p2 = 0
for a, b in fresh:
    p2 += b - a + 1


aoc.output(p1)
aoc.output(p2)
