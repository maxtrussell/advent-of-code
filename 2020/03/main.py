import typing as t

def count_trees(map: t.List[str], down: int, right: int) -> int:
    x, y = 0, 0
    count = 0
    while y < len(map):
        row = map[y]
        if row[x % len(row)] == '#':
            count += 1
        x += right
        y += down
    return count

with open('input.txt', 'rt') as f:
    data = [line.strip() for line in f.readlines()]

# Part 1
num_trees = count_trees(data, 1, 3)
print(f'Part 1: {num_trees}')

# Part 2
slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
product = 1
for slope in slopes:
    product *= count_trees(data, *slope)
print(f'Part 2: {product}')
