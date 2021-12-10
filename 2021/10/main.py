import fileinput

my_input = [l.strip() for l in fileinput.input()]

points = {')': 3, ']': 57, '}': 1197, '>': 25137, '(': 1, '[': 2, '{': 3, '<': 4}
openings = {'(': ')', '[': ']', '<': '>', '{': '}'}
corrupted = []
bracket_stacks = []
for line in my_input:
    bracket_stack = []
    for c in line:
        if c in openings:
            bracket_stack.append(c)
        else:
            if c != openings[bracket_stack[-1]]:
                # Corrupted
                corrupted.append(c)
                break
            bracket_stack.pop()
    else: 
        # Incomplete
        bracket_stacks.append(bracket_stack)

# Part 1
print(sum([points[x] for x in corrupted]))

scores = []
for bs in bracket_stacks:
    score = 0
    for c in bs[::-1]:
        score *= 5
        score += points[c]
    scores.append(score)

# Part 2
print(sorted(scores)[len(scores)//2])
