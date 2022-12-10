import aoc

dirs = {'U': (0, 1), 'R': (1, 0), 'D': (0, -1), 'L': (-1, 0)}

class Point:
    def __init__(self, x, y, track=False):
        self.x, self.y = x, y
        self.track = track
        self.seen = {(0, 0)}

    def is_adjacent(self, o):
        return max(abs(self.x - o.x), abs(self.y - o.y)) <= 1

    def do_move(self, other):
        self.x += other.x
        self.y += other.y
        self.seen.add((self.x, self.y))

def sign(x):
    if x == 0: return 0
    return 1 if x > 0 else -1

def get_move(head, tail):
    if head.is_adjacent(tail):
        return Point(0, 0)
    return Point(sign(head.x - tail.x), sign(head.y - tail.y))

def simulate(n, moves):
    knots = [Point(0, 0, i == n-1) for i in range(n)]
    for move in moves:
        knots[0].do_move(move)
        for head, tail in zip(knots, knots[1:]):
            tail.do_move(get_move(head, tail))
    return knots

# Parse input
moves: list[Point] = []
for d, qty in map(lambda l: l.split(' '), aoc.input_lines()):
    moves.extend([Point(*dirs[d]) for _ in range(int(qty))])

# Part 1
knots = simulate(2, moves)
print(len(knots[-1].seen))

# Part 2
knots = simulate(10, moves)
print(len(knots[-1].seen))
