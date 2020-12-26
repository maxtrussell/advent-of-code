import sys

def solve(key, start):
    i, loop = 1, 0
    while i != key:
        i = (start * i) % 20201227
        loop += 1
    return loop

with open(sys.argv[1]) as f:
    pk1, pk2 = [int(line.strip()) for line in f]

# Part 1
loop2 = solve(pk2, 7)
answer = pow(pk1, loop2) % 20201227
print(f'Part 1: {answer}')
