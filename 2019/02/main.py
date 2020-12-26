import sys

# maps op code to number of args and function
ops = {
    1:  (2, lambda x, y: x + y),
    2:  (2, lambda x, y: x * y),
}

def run(prog, debug=False):
    pc = 0
    while True:
        op_code = prog[pc]
        if op_code == 99:
            break

        num_args, op = ops[op_code]
        arg_ptrs = [prog[pc+i] for i in range(1, num_args+1)]
        args = [prog[ptr] for ptr in arg_ptrs]
        ret_ptr = prog[pc+num_args+1]
        prog[ret_ptr] = op(*args)

        if debug:
            # This will be useful in the future :)
            print('--- Debug ---')
            print(f'PC: {pc}')
            print(f'Op code: {op_code}')
            print(f'Arg addresses: {arg_ptrs}')
            print(f'Args: {args}')
            print(f'Return address: {ret_ptr}')
            print('---')

        # Advance pointer
        pc += 2 + num_args
    return pc, prog

def part2(prog, target):
    for x in range(0,100):
        for y in range(0, 100):
            prog[1], prog[2] = x, y
            _, output = run(prog[:])
            if output[0] == target:
                return x,y

with open(sys.argv[1]) as f:
    prog = [int(num) for num in f.read().strip().split(',')]

# Part 1
prog_copy = prog[:]
prog_copy[1] = 12
prog_copy[2] = 2
_, output = run(prog_copy)
print(f'Part 1: {output[0]}')

# Part 2
x, y = part2(prog[:], 19690720)
print(f'Part 2: {(x * 100) + y}')
