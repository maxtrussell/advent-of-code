from operator import eq, ne
import fileinput

def get_gamma(rows):
    bits = len(rows[0])
    freqs = []
    for i in range(bits):
        col = (r[i] for r in rows)
        freqs.append(1 if sum(map(lambda x: 1 if x == '1' else -1, col)) > 0 else 0)

    # Bit shifted instead of int casting for fun
    gamma = 0
    for col in freqs:
        gamma = (gamma << 1) | col
    epsilon = gamma ^ int('1' * bits, 2)
    return gamma, epsilon

def filter_rows(rows, bit):
    candidates = rows[:]
    i = 0
    while len(candidates) > 1:
        count = sum(1 if row[i] == '1' else -1 for row in candidates)
        selector = eq if count >= 0 else ne
        candidates = list(filter(lambda x: selector(x[i], bit), candidates))
        i += 1
    return int(candidates[0], 2)

my_input = [l.strip() for l in fileinput.input()]
gamma, epsilon = get_gamma(my_input)
print(f'Part 1: {gamma * epsilon}')
o2, co2 = filter_rows(my_input, '1'), filter_rows(my_input, '0')
print(f'Part 2: {o2 * co2}')
