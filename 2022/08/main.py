import aoc

from functools import reduce
from operator import mul

def get_visible(view):
    l_to_r = get_visible_one_dir(view)
    r_to_l = get_visible_one_dir(view[::-1])[::-1]
    return [ltr or rtl for ltr, rtl in zip(l_to_r, r_to_l)]

def get_visible_one_dir(view):
    visible = []
    tallest = -1
    for tree in view:
        visible.append(tree > tallest)
        tallest = max(tallest, tree)
    return visible

def scenic_score(x, y, grid):
    col = [row[x] for row in grid]
    views = [grid[y][:x][::-1], grid[y][x+1:], col[:y][::-1], col[y+1:]]  # [l, r, u, d]
    return reduce(mul, [score(grid[y][x], view) for view in views], 1)

def score(curr, view):
    i = 0
    for i, tree in enumerate(view, start=1):
        if tree >= curr:
            break
    return i
    

grid = [[int(x) for x in line] for line in aoc.input_lines()]
visible = [[False for _ in row] for row in grid]

# Rows
for y in range(len(grid)):
    visible[y] = get_visible(grid[y])

# Columns
for x in range(len(grid[0])):
    col_visible = get_visible([row[x] for row in grid])
    for y, is_visible in enumerate(col_visible):
        visible[y][x] = visible[y][x] or is_visible

visible_trees = sum(sum(row) for row in visible)
print('Part 1: ', visible_trees)

max_score = max(scenic_score(x, y, grid) for y in range(len(grid)) for x in range(len(grid[y])))
print('Part 2: ', max_score)
