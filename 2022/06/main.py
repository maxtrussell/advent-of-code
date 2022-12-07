import aoc

data = aoc.input_lines()[0]

def first_signal(n):
    i = 0
    while i < len(data) - n and not is_unique(data, i, n):
        i += 1
    return i + n

def is_unique(s, i, n):
    return len(set(data[i:i+n])) == n

print('Part 1: ', first_signal(4))
print('Part 2: ', first_signal(14))
