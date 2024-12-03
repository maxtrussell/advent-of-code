import lib.aoc as aoc

import re

p1, p2 = 0, 0
do = True
for line in aoc.input_lines():
    for match in re.findall(
        "mul\(([\d]{1,3}),([\d]{1,3})\)|(do)\(\)|(don't)\(\)", line
    ):
        if match[2] == "do":
            do = True
        elif match[3] == "don't":
            do = False
        else:
            p1 += int(match[0]) * int(match[1])
            if do:
                p2 += int(match[0]) * int(match[1])

aoc.output(p1)
aoc.output(p2)
