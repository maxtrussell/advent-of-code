import aoc

moves = {
    'A': 0, 'X': 0,
    'B': 1, 'Y': 1,
    'C': 2, 'Z': 2,
}

turns = []
for line in aoc.input_lines():
    turns.append(line.split(' '))

# Part 1
score1 = 0
for a, b in turns:
    a, b = moves[a], moves[b]
    score1 += b + 1
    if (a + 1) % 3 == b:
        score1 += 6
    elif a == b:
        score1 += 3

# Part 2
outcomes = {'X': 'lose', 'Y': 'draw', 'Z': 'win'}
score2 = 0
for a, b in turns:
    a = moves[a]
    if outcomes[b] == 'win':
        score2 += 6
        b = (a + 1) % 3
    elif outcomes[b] == 'draw':
        score2 += 3
        b = a
    elif outcomes[b] == 'lose':
        b = (a - 1) % 3
    score2 += b + 1

print('Part 1:', score1)
print('Part 2:', score2)
