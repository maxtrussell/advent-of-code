
def run(prog, part1=False):
    acc, pc = 0, 0
    visited = set()
    while True:
        if pc == len(prog):
            return acc
        elif pc in visited:
            return acc if part1 else None
        cmd, arg = prog[pc].split(' ')
        if cmd == 'acc':
            acc += int(arg)
        elif cmd == 'jmp':
            pc += int(arg)
            continue
        visited.add(pc)
        pc += 1

def fix_loop(prog):
    # Brute force :)
    for i in range(len(prog)):
        prog_copy = prog[:]
        cmd, arg = prog_copy[i].split(' ')
        if cmd == 'jmp':
            prog_copy[i] = f'nop {arg}'
        elif cmd == 'nop':
            prog_copy[i] = f'jmp {arg}'
        else:
            # No need to run
            continue
        if (acc := run(prog_copy)):
            return acc
        
with open('input.txt', 'rt') as f:
    prog = f.readlines()

# Part 1
acc = run(prog, part1=True)
print(f'Part 1: {acc}')

# Part 2
acc = fix_loop(prog)
print(f'Part 2: {acc}')
