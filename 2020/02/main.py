import typing as t

def validate_password_part_1(start: int, end: int, char: str, password: str) -> bool:
    num_range = range(start, end + 1)
    return count_char(char, password) in num_range

def validate_password_part_2(first: int, second: int, char: str, password: str) -> bool:
    i, j = first - 1, second - 1  # convert to 0 based index
    if i == j:
        return password[i] == char
    return (password[i] == char) ^ (password[j] == char)  # xor

def count_char(char: str, s: str) -> int:
    count = 0
    for c in s:
        if c == char:
            count += 1
    return count

def parse_line(line: str) -> t.Tuple[int, int, str, str]:
    parts = line.split(' ')

    if '-' in parts[0]:
        start, end = parts[0].split('-')
    else:
        start = end = parts[0]
    start, end = int(start), int(end)

    char = parts[1][0]
    password = parts[2]
    return (start, end, char, password)

with open('input.txt', 'rt') as f:
    data = [parse_line(line.strip()) for line in f.readlines()]

valid_passwords = [line for line in data if validate_password_part_1(*line)]
print(f'Part 1: {len(valid_passwords)}')

valid_passwords = [line for line in data if validate_password_part_2(*line)]
print(f'Part 2: {len(valid_passwords)}')
