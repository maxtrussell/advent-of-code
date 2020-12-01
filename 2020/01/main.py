import typing as t

def two_sum(data: t.List[int], sum: int) -> t.Tuple[int, int]:
    diffs = set()
    for entry in data:
        diff = sum - entry
        if diff in diffs:
            return (entry, diff)
        diffs.add(entry)
    return (-1, -1)

def three_sum(data: t.List[int], sum: int) -> t.Tuple[int, int, int]:
    for i in range(0,len(data)):
        entry = data[i]
        diff = sum - entry
        x, y = two_sum(data[i+1:], diff)
        if x > 0:
            return (entry, x, y)
    return (-1, -1)


data = []
with open('input.txt', 'rt') as f:
    for line in f:
        if line.strip() != '':
            data.append(int(line.strip()))

# Part 1
x, y = two_sum(data, 2020)
print(f"Part 1: {x * y}")

# Part 2
x, y, z = three_sum(data, 2020)
print(f"Part 2: {x * y * z}")
