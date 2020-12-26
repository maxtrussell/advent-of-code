def calculate_fuel(mass, recurse=False):
    fuel = (mass // 3) - 2
    if recurse and fuel > 0:
        fuel += calculate_fuel(fuel, recurse=recurse)
    return fuel if fuel > 0 else 0

with open('input.txt') as f:
    lines = [int(l.strip()) for l in f]

# Part 1
fuel = sum([calculate_fuel(m) for m in lines])
print(f'Part 1: {fuel}')

# Part 2
fuel = sum([calculate_fuel(m, recurse=True) for m in lines])
print(f'Part 2: {fuel}')
