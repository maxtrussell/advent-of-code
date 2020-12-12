import math
import sys

cardinal = {
    'N': (0, 1),
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0),
}

turn = {'L': 1, 'R': -1}

class Position:
    def __init__(self, x, y, bearing=0):
        self.x = x
        self.y = y
        self.bearing = bearing

    def __repr__(self):
        return f'({self.x}, {self.y}), {self.bearing}'

def navigate(pos, instruction):
    cmd, magnitude = instruction[0], int(instruction[1:])
    if (dir := cardinal.get(cmd, None)):
        pos.x += dir[0] * magnitude
        pos.y += dir[1] * magnitude
    elif (dir := turn.get(cmd, None)):
        pos.bearing += dir * magnitude
    else:
        # Forward
        pos.x += round(magnitude * math.cos(math.radians(pos.bearing)), 2)
        pos.y += round(magnitude * math.sin(math.radians(pos.bearing)), 2)
    return pos

def waypoint_nav(ship, waypoint, instruction):
    cmd, magnitude = instruction[0], int(instruction[1:])
    if (dir := cardinal.get(cmd, None)):
        waypoint.x += dir[0] * magnitude
        waypoint.y += dir[1] * magnitude
    elif cmd in turn:
        # since turns are only in 90 degree increments
        for _ in range(magnitude // 90):
            if cmd == 'R':
                waypoint.x, waypoint.y = waypoint.y, waypoint.x * -1
            else:
                waypoint.x, waypoint.y = waypoint.y * -1, waypoint.x
    else:
        # Forward
        ship.x += waypoint.x * magnitude
        ship.y += waypoint.y * magnitude
    return (ship, waypoint)


input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'rt') as f:
    steps = f.readlines()

# Part 1
pos = Position(0, 0, 0)  # facing east
for s in steps:
    pos = navigate(pos, s)
print(f'Part 1: {abs(pos.x) + abs(pos.y)}')

# Part 2
ship = Position(0, 0)
waypoint = Position(10, 1)
for s in steps:
    ship, waypoint = waypoint_nav(ship, waypoint, s)
print(f'Part 2: {abs(ship.x) + abs(ship.y)}')
 
