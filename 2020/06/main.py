def unique_questions_answered(group: str) -> int:
    return len({q for q in group if q != '\n'})

def common_questions_answered(group: str) -> int:
    questions = {}
    for q in group:
        if q != '\n':
            questions[q] = questions.get(q, 0) + 1
    return len([q for q,num in questions.items() if num == len(group.split('\n'))])

with open('input.txt', 'rt') as f:
   groups = [l.strip() for l in f.read().split('\n\n')]

# Part 1
answered = [unique_questions_answered(g) for g in groups]
print(f'Part 1: {sum(answered)}')

# Part 2
common = [common_questions_answered(g) for g in groups]
print(f'Part 2: {sum(common)}')
