import aoc

from collections import deque
import re

def do_move(layout, qty, src, dst, keep_order):
    buf = deque()
    for _ in range(qty):
        buf.append(layout[src].pop())

    while buf:
        if keep_order:
            layout[dst].append(buf.pop())
        else:
            layout[dst].append(buf.popleft())

m = aoc.input_lines().index('')

# Parse container layout
layout_lines = aoc.input_lines(strip=False)[:m]
num_cols = int(layout_lines[-1].split()[-1])
layout = [deque() for _ in range(num_cols)]
for line in layout_lines[:-1]:
    for i, c in enumerate(line):
        if not c.isspace() and (i-1) % 4 == 0:
            layout[(i-1) // 4].appendleft(c)

# Parse moves
move_lines = aoc.input_lines()[m+1:]
moves = []
for line in move_lines:
    m = re.match(r'move (\d+) from (\d+) to (\d+)', line)
    qty, src, dst = [int(x) for x in m.groups()]
    moves.append((qty, src-1, dst-1))

# Simulate
for part, keep_order in enumerate([False, True], start=1):
    curr_layout = [col.copy() for col in layout]
    for qty, src, dst in moves:
        do_move(curr_layout, qty, src, dst, keep_order)

    tops = ''.join([col[-1] for col in curr_layout])
    print(f'Part {part}: {tops}')
