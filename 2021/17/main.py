def in_target(px, py, target_max, target_min):
    max_x, max_y = target_max
    min_x, min_y = target_min
    return (min_x <= px <= max_x) and (min_y <= py <= max_y)

def fire_probe(vx, vy, target_max, target_min):
    max_height = 0
    px, py = (0, 0)
    while (px <= target_max[0]) and (py >= target_min[1]):
        max_height = max(py, max_height)
        if in_target(px, py, target_max, target_min):
            return True, max_height
        px += vx
        py += vy
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1
    return False, max_height

def calculate_max_x(dx):
    return (dx * (dx + 1)) / 2

"""
max distance x = (vx * (vx + 1)) / 2
"""

target_max = (318, -53)
target_min = (277, -92)

# Calculate velocity bounds
min_vx = 0
max_vx = target_max[0]
min_vy = target_min[1]
max_vy = abs(target_min[1]) - 1

print('Part 1', (target_min[1] * (target_min[1] + 1)) // 2)

hits = 0
for vx in range(min_vx, max_vx+1):
    for vy in range(min_vy, max_vy+1):
        hit_target, _ = fire_probe(vx, vy, target_max, target_min)
        if hit_target:
            hits += 1
print(f'Part 2: {hits}')
