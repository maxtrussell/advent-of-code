import aoc

from collections import deque
from copy import deepcopy
from operator import add, mul

class Monkey:
    def __init__(self, items, op, arg, test, targets):
        self.items = items
        self.op = op
        self.arg = arg
        self.test = test
        self.targets = targets
        self.inspected = 0

    def do_turn(self):
        outbound = []
        while self.items:
            self.inspect()
            outbound.append(self.throw())
        return outbound

    def inspect(self):
        self.inspected += 1
        arg = self.arg or self.items[0]
        
        global part
        if part == 1:
            self.items[0] = self.op(self.items[0], arg) // 3
        else:
            global lcm
            self.items[0] = self.op(self.items[0], arg) % lcm

    def throw(self):
        item = self.items.popleft()
        target = self.targets[int(item % self.test != 0)]
        return item, target

def last_int(line):
    return int(line.split(' ')[-1])

# Parse input
original_monkeys = []
lcm = 1
for m in aoc.raw_input().split('\n\n'):
    monkey_lines = [l.strip() for l in m.split('\n') if l.strip()]
    _, start_l, op_l, test_l, true_l, false_l = monkey_lines
    items = [int(n) for n in start_l.split(': ')[1].split(', ')]

    op = add if '+' in op_l else mul
    arg = op_l.split(' ')[-1]
    arg = None if arg == 'old' else int(arg)
    test = last_int(test_l)
    lcm *= test
    targets = [last_int(true_l), last_int(false_l)]
    original_monkeys.append(Monkey(deque(items), op, arg, test, targets))

# Simulate rounds
for part, rounds in enumerate([20, 10000], start=1):
    monkeys = deepcopy(original_monkeys)
    for _ in range(rounds):
        for m in monkeys:
            for item, recipient in m.do_turn():
                monkeys[recipient].items.append(item)
    
    m1, m2 = sorted(monkeys, key=lambda m: m.inspected, reverse=True)[:2]
    print(f'Part {part}:', m1.inspected * m2.inspected)
