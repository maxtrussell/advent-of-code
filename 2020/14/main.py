import itertools
import sys
import re

def run(lines, part2=False):
    mem = {}
    for line in lines:
        if line.startswith('mask'):
            mask = line.split(' = ')[1]
        else:
            addr, val = re.match('mem\[(\d+)\] = (\d+)', line).groups()
            if not part2:
                mem[int(addr)] = apply_val_mask(int(val), mask)
            else:
                mem |= {to_int(a):int(val) for a in apply_addr_mask(to_bits(int(addr)), mask)}
    return mem

def to_bits(decimal):
    return [int(c) for c in f'{decimal:036b}']

def to_int(binary):
    return int(''.join([str(b) for b in binary]), 2)
            
def apply_val_mask(val, mask):
    val |= int(mask.replace('X', '0'), 2)
    val &= int(mask.replace('X', '1'), 2)
    return val

def apply_addr_mask(addr, mask):
    # This turned out a little messier than I would have liked
    combinations = itertools.product('10', repeat=mask.count('X'))
    addrs = []
    for combination in combinations:
        j = 0
        new_addr = addr[:]
        for i in range(len(mask)):
            if mask[i] == 'X':
                new_addr[i] = combination[j]
                j += 1
            elif mask[i] == '1':
                new_addr[i] = mask[i]
        addrs.append(new_addr)
    return addrs
            
input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
with open(input_file, 'rt') as f:
    lines = [l.strip() for l in f.readlines()]

# Part 1
mem = run(lines)
total = sum(mem.values())
print(f'Part 1: {total}')

# Part 2
mem = run(lines, part2=True)
total = sum(mem.values())
print(f'Part 2: {total}')
