import math
import sys

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

def play_game(start, num_cups, num_turns):
    # Create nodes
    nodes = {}
    # Add starting cups to linked list
    for i in range(len(start)):
        val = start[i]
        nodes[val] = Node(val)
        if i-1 >= 0:
            nodes[start[i-1]].next = nodes[val]

    if num_cups == len(start):
        # link last node to starting node
        nodes[start[-1]].next = nodes[start[0]]
    else:
        # Add additional cups if necessary
        for x in range(len(start)+1, num_cups+1):
            nodes[x] = Node(x)
            if x > len(start)+1:
                nodes[x-1].next = nodes[x]

        # link start and rest of nodes together
        nodes[start[-1]].next = nodes[len(start)+1]

        # link last node to first node
        nodes[num_cups].next = nodes[start[0]]

    head = nodes[start[0]]
    for t in range(num_turns):
        # Progress bar, just for fun
        if num_turns > 1000 and t % 1000 == 0:
            progress = math.ceil((t / num_turns) * 30)
            end = '\r' if t + 1000 < num_turns else '\n'
            print(f'Progress [{progress * "="}{(30-progress) * " "}]', end=end)

        # Find destination cup
        pickup = [head.next, head.next.next, head.next.next.next]
        dst = head.val - 1 if head.val > 1 else num_cups
        while dst in [n.val for n in pickup]:
            dst -= 1
            if dst < 1:
                dst = num_cups

        # "picks up" cups
        head.next = pickup[-1].next

        # Moves picked up cups after destination cup
        pickup[-1].next = nodes[dst].next
        nodes[dst].next = pickup[0]

        head = head.next

    x, y = nodes[1].next.val, nodes[1].next.next.val
    return (head, nodes[1].next.val * nodes[1].next.next.val)

def stringify_cups(cups):
    i = cups.index(1)
    return ''.join(
        list(map(str, filter(lambda x: x != 1, [cups[(i+j) % 9] for j in range(9)])))
    )

with open(sys.argv[1]) as f:
    start = [int(x) for x in f.read().strip()]

# Part 1
head, _ = play_game(start[:], 9, 100)
cups = []
for _ in range(9):
    cups.append(head.val)
    head = head.next
print(f'Part 1: {stringify_cups(cups)}')
    

# Part 2
_, part2 = play_game(start[:], 1000000, 10000000)
print(f'Part 2: {part2}')
