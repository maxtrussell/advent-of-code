import sys

elves = []
with open(sys.argv[1]) as f:
    for elf in f.read().split('\n\n'):
        elves.append(sum([int(x) for x in elf.split('\n') if x]))

elves = sorted(elves, reverse=True)
print(f'Part 1: {elves[0]}')
print(f'Part 2: {sum(elves[:3])}')
