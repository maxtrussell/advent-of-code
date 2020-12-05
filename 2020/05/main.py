import math
import typing as t

def find_seat(line: str) -> int:
    col_min, col_max = 0, 7
    min, max = 0, 127
    row = binary_search(line, 'F', 'B', 0, 127)
    col = binary_search(line, 'L', 'R', 0, 7)
    return (row * 8) + col

def binary_search(line: str, lower: str, higher: str, min: int, max: int) -> int:
    for c in line:
        if c == lower:
            max -= math.floor((max - min) / 2)
        elif c == higher:
            min += math.ceil((max - min) / 2)
    return max if line[-1] == lower else min

def find_my_seat(seats: t.List[int]) -> int:
    # discard first and last rows of seats
    valid_ids = {s for s in seats if 7 < s < 1016}
    i = 0
    while i < 1016:
        if i not in valid_ids and i - 1 in valid_ids and i + 1 in valid_ids:
            return i
        i += 1
    return -1


with open('input.txt', 'rt') as f:
    lines = [l for l in f.readlines()]

# Part 1
seat_ids = [find_seat(l) for l in lines]
print(f'Part 1: {max(seat_ids)}')

# Part 2
print(f'Part 2: {find_my_seat(seat_ids)}')
