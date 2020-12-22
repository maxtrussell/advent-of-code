import sys

def recursive_combat(p1, p2, part2=True):
    prev_states = set()
    while p1 and p2:
        if part2:
            state = (tuple(p1), tuple(p2))
            if state in prev_states:
                # immediate win for p1
                return ('Player1', p1)
            prev_states.add(state)

        # Draw cards
        card1, card2 = p1.pop(), p2.pop()
        if part2 and len(p1) >= card1 and len(p2) >= card2:
            # Recurse!
            new_p1 = [p1[-i-1] for i in range(card1)][::-1]
            new_p2 = [p2[-i-1] for i in range(card2)][::-1]
            p1_wins, _ = recursive_combat(new_p1, new_p2)
        else:
            p1_wins = card1 > card2

        if p1_wins:
            p1 = [card2, card1] + p1
        else:
            p2 = [card1, card2] + p2
    return (True if p1 else False, p1 if p1 else p2)

def calculate_score(deck):
    scores = [deck[i] * (i + 1) for i in range(0, len(deck))]
    return sum(scores)

with open(sys.argv[1]) as f:
    p1, p2 = [
        [int(c) for c in ''.join(p).splitlines()[1:][::-1]]
        for p in f.read().split('\n\n')
    ]

# Part 1
_, winning_deck = recursive_combat(p1[:], p2[:], part2=False)
print(f'Part 1: {calculate_score(winning_deck)}')

# Part 2
_, winning_deck = recursive_combat(p1[:], p2[:])
print(f'Part 2: {calculate_score(winning_deck)}')
