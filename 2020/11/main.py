import itertools

def simulate_full(data, move_threshold, detected):
    prev, curr = data, simulate_round(data, move_threshold, detected)
    while prev != curr:
        prev, curr = curr, simulate_round(curr, move_threshold, detected)
    return curr

def simulate_round(data, move_threshold, occupied):
    new_data = [row[:] for row in data[:]]
    neighbors = [(x, y) for x,y in itertools.product([-1, 0, 1], repeat=2) if not x == y == 0]
    for row in range(len(data)):
        for col in range(len(data[row])):
            curr_seat = data[row][col]
            if curr_seat == '.':
                # Floor never changes :)
                continue
            occupied_neighbors = len([(dy, dx) for dy,dx in neighbors if occupied(data, row, col, dy, dx)])
            if curr_seat == 'L' and occupied_neighbors == 0:
                # empty -> occupied
                new_data[row][col] = '#'
            elif curr_seat == '#' and occupied_neighbors >= move_threshold:
                # occupied -> empty
                new_data[row][col] = 'L'
    return new_data

def is_occupied(data, r, c, delta_y, delta_x):
    if r+delta_y in range(len(data)) and c+delta_x in range(len(data[r+delta_y])):
        return data[r+delta_y][c+delta_x] == '#'
    return False

def see_occupied(data, r, c, dir_y, dir_x, tiles_looked=1):
    delta_y = dir_y * tiles_looked
    delta_x = dir_x * tiles_looked 
    if r+delta_y in range(len(data)) and c+delta_x in range(len(data[r+delta_y])):
        tile = data[r+delta_y][c+delta_x]
        if tile == '.':
            # keep looking
            return see_occupied(data, r, c, dir_y, dir_x, tiles_looked+1)
        else:
            return tile == '#'
    # out of bounds
    return False

with open('input.txt', 'rt') as f:
    lines = [list(l.strip()) for l in f.readlines()]

# Part 1
stable = simulate_full(lines, 4, is_occupied)
occupied = sum([row.count('#') for row in stable])
print(f'Part 1: {occupied}')

# Part 2
stable = simulate_full(lines, 5, see_occupied)
occupied = sum([row.count('#') for row in stable])
print(f'Part 2: {occupied}')
