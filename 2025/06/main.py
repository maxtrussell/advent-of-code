import lib.aoc as aoc

from math import prod
import re

lines = aoc.input_lines(strip=False)
ops = lines[-1].split()

p1_problems = []
p1_problems = [[] for _ in range(len(lines[0].split(" ")))]
for line in lines[:-1]:
    for i, col in enumerate(line.split()):
        p1_problems[i].append(int(col))

i = 0
p2_problems = [[] for _ in range(len(lines[0].split()))]
for x in range(len(lines[0])):
    num = ""
    for y in range(len(lines)):
        num += lines[y][x]

    num = re.sub(r"\D", "", num)
    if num:
        p2_problems[i].append(int(num))
    else:
        i += 1

for problems in [p1_problems, p2_problems]:
    ans = 0
    for nums, op in zip(problems, ops):
        if op == "*":
            ans += prod(nums)
        else:
            ans += sum(nums)
    aoc.output(ans)
