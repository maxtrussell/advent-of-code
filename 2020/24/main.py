import collections
import sys

def parse_line(line):
    directions = []
    lookahead = False
    for i in range(len(line)):
        if lookahead:
            lookahead = False
            directions.append(line[i-1:i+1])
        elif line[i] == 'e' or line[i] == 'w':
            directions.append(line[i])
        else:
            lookahead = True
    return directions

def flip_tile(direction):
    """
    NOTE: Using the double cord system described here:
    https://www.redblobgames.com/grids/hexagons/
    """
    x, y = 0, 0
    for dir in direction:
        if dir == 'e':
            x +=2
        elif dir == 'w':
            x -=2
        elif dir == 'ne':
            x += 1
            y += 1
        elif dir == 'nw':
            x -= 1
            y += 1
        elif dir == 'se':
            x += 1
            y -= 1
        elif dir == 'sw':
            x -= 1
            y -= 1
    return (x, y)

def round(black_tiles):
    """ Same gist from conway cube day """
    new_black_tiles = set()
    neighbors = [(-1,1), (1,1), (2,0), (1,-1), (-1,-1), (-2,0)]
    potential_changes = set()
    for x,y in black_tiles:
        for dx,dy in neighbors:
            potential_changes.add((x+dx,y+dy))
    potential_changes |= black_tiles

    for x,y in potential_changes:
        black_neighbors = len([True for dx,dy in neighbors if (x+dx,y+dy) in black_tiles])
        if (x,y) in black_tiles and black_neighbors in {1, 2}:
            new_black_tiles.add((x,y))
        elif (x,y) not in black_tiles and black_neighbors == 2:
            new_black_tiles.add((x,y))
    return new_black_tiles

with open(sys.argv[1]) as f:
    directions = [parse_line(l.strip()) for l in f]

# Part 1
tiles = collections.defaultdict(lambda: 0)
for dir in directions:
    tiles[flip_tile(dir)] += 1
black_tiles = {cords for cords,flips in tiles.items() if flips % 2 == 1}
print(f'Part 1: {len(black_tiles)}')

# Part 2
for _ in range(100):
    black_tiles = round(black_tiles)
print(f'Part 2: {len(black_tiles)}')
