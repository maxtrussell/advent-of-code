import lib.aoc as aoc

from collections import defaultdict


def fix_update(
    update: set[int], seen: set[int], fixed: list[int], rules: dict[int, set]
) -> list[int]:
    if len(fixed) == len(update):
        return fixed

    for x in (y for y in update if y not in seen):
        need_before = (rules[x] - seen) & update
        if not need_before:
            fixed.append(x)
            seen.add(x)
            return fix_update(update, seen, fixed, rules)
    assert False


parse_rules = True
rules = defaultdict(set)
p1, p2 = 0, 0
for line in aoc.input_lines():
    if not line:
        parse_rules = False
    elif parse_rules:
        l, r = (int(x) for x in line.split("|"))
        rules[r].add(l)
    else:
        update = [int(x) for x in line.split(",")]
        fixed = fix_update(set(update), set(), [], rules)
        if update == fixed:
            p1 += update[len(update) // 2]
        else:
            p2 += fixed[len(fixed) // 2]

aoc.output(p1)
aoc.output(p2)
