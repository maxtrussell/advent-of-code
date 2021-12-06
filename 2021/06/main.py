import collections
import fileinput

fish = collections.Counter(map(int, fileinput.input()[0].split(',')))
days = 256
for i in range(days):
    new_fish = collections.Counter()
    for age, count in fish.items():
        if age == 0:
            new_fish[6] += count
            new_fish[8] += count
        else:
            new_fish[age-1] += count
    fish = new_fish
    if i == 79:
        print('Part 1:', sum(fish.values()))
print('Part 2:', sum(fish.values()))
