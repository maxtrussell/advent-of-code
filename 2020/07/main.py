import collections
import re

def parse_input(path):
    contains = collections.defaultdict(dict)
    containedin = collections.defaultdict(set)
    with open(path, 'rt') as f:
        for line in f.readlines():
            outer_color = re.match('([a-z ]+) bags contain', line)[1]
            for count, inner_color in re.findall('(\d+) ([a-z ]+) bag', line):
                containedin[inner_color].add(outer_color)
                contains[outer_color][inner_color] = int(count)
    return contains, containedin

def holds_target(target, contains, containedin):
    outer_bags = set()
    for bag in containedin[target]:
        # add immediate bag
        outer_bags.add(bag)

        # add parent bags
        outer_bags |= holds_target(bag, contains, containedin)
    return outer_bags

def must_hold(target, contains, containedin):
    inner_bags = 0
    for bag, count in contains[target].items():
        # add immediate bags
        inner_bags += count

        # add nested bags
        inner_bags += count * must_hold(bag, contains, containedin)
    return inner_bags
        

contains, containedin = parse_input('input.txt')

# Part 1
outer_bags = holds_target('shiny gold', contains, containedin)
print(f'Part 1: {len(outer_bags)}')

# Part 2
inner_bags = must_hold('shiny gold', contains, containedin)
print(f'Part 2: {inner_bags}')
