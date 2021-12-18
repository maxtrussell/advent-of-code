import json
import fileinput
from functools import reduce
from itertools import permutations
from math import ceil

def add_next(elem, next, left):
    if next is None:
        return elem
    elif isinstance(elem, int):
        return elem + next
    a, b = elem
    if left:
        return [add_next(a, next, left), b]
    else:
        return [a, add_next(b, next, left)]

def explode(elem, depth=0):
    if isinstance(elem, int):
        return False, None, elem, None
    a, b = elem
    if depth == 4:
        return True, a, 0, b
    exploded, left, a, right = explode(a, depth+1)
    if exploded:
        return True, left, [a, add_next(b, right, left=True)], None
    exploded, left, b, right = explode(b, depth+1)
    if exploded:
        return True, None, [add_next(a, left, left=False), b], right
    return False, None, elem, None
    

def split(elem):
    if isinstance(elem, int):
        if elem >= 10:
            return True, [elem // 2, ceil(elem / 2)]
        return False, elem

    a, b = elem
    did_split, new = split(a)
    if did_split:
        return True, [new, b]
    did_split, new = split(b)
    if did_split:
        return True, [a, new]
    return False, elem

# Track index of current element
def snail_reduce(a, b, depth=0):
    elem = [a, b]
    while True:
        changed = False

        # First try to explode
        changed, _, elem, _ = explode(elem)
        if changed:
            continue

        # Second try to split
        changed, elem = split(elem)
        if changed:
            continue

        return elem

def magnitude(elem):
    if isinstance(elem, int):
        return elem
    a, b = elem
    return 3*magnitude(a) + 2*magnitude(b)
        

# json.loads is much safer than eval :)
lines = [json.loads(l.strip()) for l in fileinput.input()]
print(magnitude(reduce(snail_reduce, lines)))
max_sum = 0
for a,b in permutations(lines, 2):
    max_sum = max(magnitude(snail_reduce(a, b)), max_sum)
print(max_sum)
