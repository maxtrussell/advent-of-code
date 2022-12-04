import aoc

def get_priority(item):
    if item.isupper():
        return ord(item) - 38
    return ord(item) - 96

compartments = []
rucksacks = []
for line in aoc.input_lines():
    m = len(line) // 2
    compartments.append((set(line[:m]), set(line[m:])))
    rucksacks.append(set(line))

# Part 1
overlaps = [(a & b).pop() for a, b in compartments]
print('Part 1: ', sum(map(get_priority, overlaps)))

# Part 2
badges = []
i = 0
while i+3 <= len(rucksacks):
    a, b, c = rucksacks[i:i+3]
    badges.append(a.intersection(b, c).pop())
    i += 3
print('Part 2: ', sum(map(get_priority, badges)))
