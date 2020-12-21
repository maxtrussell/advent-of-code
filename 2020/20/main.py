import collections
import re
import sys

class Tile:
    def __init__(self, id, data):
        self.id = id
        self.data = data

        # Set edges, top is 0, right is 1, bottom 2, left 3
        self.edges = {0: data[0], 2: data[-1]}
        self.edges[3] = [row[0] for row in data]
        self.edges[1] = [row[-1] for row in data]

    def rotate(self):
        new_data = [row[:] for row in self.data]
        center = (len(self.data)-1) / 2
        for y, row in enumerate(self.data):
            for x, char in enumerate(row):
                cordx, cordy = x-center, y-center
                cordx, cordy = cordy * -1, cordx
                new_data[int(cordy+center)][int(cordx+center)] = char
        return Tile(self.id, new_data)

    def yflip(self):
        return Tile(self.id, [row for row in self.data[::-1]])

    def xflip(self):
        new_data = [row[:] for row in self.data]
        for y, row in enumerate(self.data):
            new_data[y] = row[::-1]
        return Tile(self.id, new_data)

    def no_borders(self):
        new_data = [[None for _ in range(len(self.data)-2)] for _ in range(len(self.data)-2)]
        for y, row in enumerate(self.data):
            if y == 0 or y == len(self.data)-1:
                continue
            for x, char in enumerate(row):
                if x == 0 or x == len(row)-1:
                    continue
                new_data[y-1][x-1] = char
        return new_data

    def string(self):
        s = ''
        for row in self.data:
            s += ''.join(row) + '\n'
        return s

    def __repr__(self):
        return str(self.id)

def parse_tile(raw_tile):
    tid = int(re.match('Tile (\d+):', raw_tile[0]).group(1))
    return Tile(tid, [list(row) for row in raw_tile[1:]])

def get_rotations(side, connecting_side):
    """ Could probably come up with a formula instead, but oh well """
    rotations = 0
    while side != (connecting_side + 2) % 4:
        side = (side + 1) % 4
        rotations += 1
    return rotations

def assemble(tiles):
    side_length = int(len(tiles) ** 0.5)
    starter = tiles[0]
    available_edges = {''.join(edge):(0,0,side) for side,edge in starter.edges.items()}
    layout = {(0,0): starter}
    assigned_tiles = {starter.id}
    while len(assigned_tiles) < len(tiles):
        for tile in tiles[1:]:
            if tile.id in assigned_tiles:
                continue
            for side, edge in tile.edges.items():
                str_edge = ''.join(edge)
                if str_edge in available_edges or str_edge[::-1] in available_edges:
                    y, x, connecting_side = available_edges[str_edge if str_edge in available_edges else str_edge[::-1]]
                    if connecting_side == 0:
                        y -= 1
                    elif connecting_side == 1:
                        x += 1
                    elif connecting_side == 2:
                        y += 1
                    elif connecting_side == 3:
                        x -= 1
                    rotations = get_rotations(side, connecting_side)
                    for _ in range(rotations):
                        tile = tile.rotate()
                    side = (rotations + side) % 4
                    str_edge = ''.join(tile.edges[side])
                    if str_edge[::-1] in available_edges:
                        tile = tile.xflip() if side in {0,2} else tile.yflip()
                        str_edge = ''.join(tile.edges.get(side))
                    new_edges = {''.join(edge):(y,x,s) for s,edge in tile.edges.items()}
                    layout[(x,y)] = tile
                    assigned_tiles.add(tile.id)
                    available_edges.update(new_edges)
                    available_edges.pop(str_edge)
                    break  # move on to next tile

    # Normalize layout for 2d array
    min_x, min_y = 0,0
    for x,y in layout:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
                
    grid = [[None for _ in range(side_length)] for _ in range(side_length)]
    for x,y in layout:
        grid[y-min_y][x-min_x] = layout[(x,y)]
    return grid

def merge_image(grid):
    image = ''
    tile_height = 8
    for i, grid_row in enumerate(grid):
        for y in range(tile_height):
            line = ''
            for tile in grid_row:
                line += ''.join(tile[y])
            image += line + '\n'
    return Tile('Final Image :)', [list(line) for line in image.splitlines()])

def find_monsters(image):
    """ Monster for reference
    ..................#.'
    #....##....##....###
    .#..#..#..#..#..#...
    """
    monster = [
        (18,0), (0,1), (5,1), (6,1), (11,1), (12,1), (17,1), (18,1), (19,1),
        (1,2), (4,2), (7, 2), (10,2), (13,2), (16,2),
    ]
    image_lines = image.string().splitlines()
    monsters = []
    for y, line in enumerate(image_lines):
        if y > len(image_lines) - 3:
            break
        for x, char in enumerate(line):
            if x > len(line) - 19:
                # no space for sea monster here
                continue
            for dx,dy in monster:
                if image_lines[y+dy][x+dx] != '#':
                    break
            else:
                monsters.append((x, y))
    return monsters
                

with open(sys.argv[1]) as f:
    raw_tiles = [t.splitlines() for t in f.read().split('\n\n') if t]
tiles = [parse_tile(t) for t in raw_tiles]

# Part 1
grid = assemble(tiles)
side_length = int(len(tiles) ** 0.5)
product = 1
for x, y in [(0,0), (0,side_length-1), (side_length-1,0), (side_length-1,side_length-1)]:
    product *= grid[y][x].id
print(f'Part 1: {product}')

# Part 2
boarderless = [[t.no_borders() for t in row] for row in grid]
image = merge_image(boarderless)
monsters = find_monsters(image)
while not monsters:
    # Rotate until a sea monster is found
    image = image.rotate()
    monsters = find_monsters(image)
rough_waters = image.string().count('#') - (len(monsters) * 15)
print(f'Part 2: {rough_waters}')
