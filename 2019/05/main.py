import sys

def advance_pc(pc, num_args):
    return pc + 1 + num_args

def add_op(pc, prog, arg_ptrs, x, y, _):
    ret_addr = arg_ptrs[-1]
    prog[ret_addr] = x + y
    return advance_pc(pc, 3)

def mult_op(pc, prog, arg_ptrs, x, y, _):
    ret_addr = arg_ptrs[-1]
    prog[ret_addr] = x * y
    return advance_pc(pc, 3)

def input_op(pc, prog, arg_ptrs, _):
    ret_addr = arg_ptrs[-1]
    prog[ret_addr] = int(input('Input:\n> '))
    return advance_pc(pc, 1)

def output_op(pc, prog, arg_ptrs, val):
    print(f'Output: {val}')
    return advance_pc(pc, 1)

def jmp_if_true(pc, prog, arg_ptrs, x, dst):
    return dst if x else advance_pc(pc, 2)

def jmp_if_false(pc, prog, arg_ptrs, x, dst):
    return dst if not x else advance_pc(pc, 2)

def less_than_op(pc, prog, arg_ptrs, x, y, _):
    ret_addr = arg_ptrs[-1]
    prog[ret_addr] = 1 if x < y else 0
    return advance_pc(pc, 3)

def equals_op(pc, prog, arg_ptrs, x, y, _):
    ret_addr = arg_ptrs[-1]
    prog[ret_addr] = 1 if x == y else 0
    return advance_pc(pc, 3)

def eval(prog, debug=False):
    pc = 0
    while True:
        instr = prog[pc]
        op_code = instr % 100
        if op_code == 99:
            break

        num_args, op = ops[op_code]
        modes = [int(x) for x in str(instr // 100)[::-1]]
        if len(modes) < num_args:
            # account for leading zeroes if needed
            modes.extend([0] * (num_args - len(modes)))

        # Get args
        arg_ptrs, args = [], []
        for i in range(num_args):
            j = i + 1
            if modes[i] == 0:
                # pointer mode
                arg_ptrs.append(prog[pc+j])
                args.append(prog[arg_ptrs[-1]])
            else:
                # immediate mode
                args.append(prog[pc+j])

        if debug:
            # This will be useful in the future :)
            print('--- Debug ---')
            print(f'PC: {pc}')
            print(f'Instr: {instr}')
            print(f'Op code: {op_code}')
            print(f'Op: {op.__name__}')
            print(f'Modes: {modes}')
            print(f'Arg addresses: {arg_ptrs}')
            print(f'Args: {args}')
            print('---')

        # Do op
        pc = op(pc, prog, arg_ptrs, *args)

    return pc, prog

# maps op code to number of args and function
ops = {
    1:  (3, add_op),
    2:  (3, mult_op),
    3:  (1, input_op),
    4:  (1, output_op),
    5:  (2, jmp_if_true),
    6:  (2, jmp_if_false),
    7:  (3, less_than_op),
    8:  (3, equals_op),
}

with open(sys.argv[1]) as f:
    prog = [int(num) for num in f.read().strip().split(',')]

# Run the program!
eval(prog[:])
