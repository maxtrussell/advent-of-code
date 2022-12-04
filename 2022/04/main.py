import aoc

def has_subset(a, b):
    return ((a[0] <= b[0] and a[1] >= b[1])
            or (b[0] <= a[0] and b[1] >= a[1]))

def has_overlap(a, b):
    return (a[0] <= b[0] <= a[1]) or (b[0] <= a[0] <= b[1])

pairs = []
for line in aoc.input_lines():
    raw_sections = line.split(',')
    sections = []
    for section in raw_sections:
        sections.append([int(x) for x in section.split('-')])
    pairs.append(sections)

num_subsets = sum(has_subset(a, b) for a, b in pairs)
num_overlaps = sum(has_overlap(a, b) for a, b in pairs)
print('Part 1: ', num_subsets)
print('Part 2: ', num_overlaps)
