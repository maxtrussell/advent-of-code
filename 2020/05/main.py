import math
import typing as t

def find_seat(line: str) -> int:
    line = line.replace('F', '0')
    line = line.replace('B', '1')
    line = line.replace('L', '0')
    line = line.replace('R', '1')
    return int(line, 2)

def find_my_seat(seats: t.List[int]) -> int:
    # discard first and last rows of seats
    for i in range(256 * 8):
        if i not in seats and i-1 in seats and i+1 in seats:
            return i
    return -1


with open('input.txt', 'rt') as f:
    lines = [l for l in f.readlines()]

# Part 1
seat_ids = [find_seat(l) for l in lines]
print(f'Part 1: {max(seat_ids)}')

# Part 2
print(f'Part 2: {find_my_seat(seat_ids)}')
