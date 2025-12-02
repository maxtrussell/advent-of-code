import lib.aoc as aoc

import re

p1, p2 = 0, 0
for id_range in aoc.input_lines()[0].split(","):
    start, end = [int(x) for x in id_range.split("-")]
    for x in range(start, end + 1):
        if re.match(r"^(\d+)\1$", str(x)):
            p1 += x
            p2 += x
        elif re.match(r"^(\d+)\1+$", str(x)):
            p2 += x

aoc.output(p1)
aoc.output(p2)
