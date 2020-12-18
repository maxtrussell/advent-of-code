import sys

def parse(expr, part1=False):
    rpn = ''
    stack = []
    for char in expr:
        # If only python had switch :/
        if char.isnumeric():
            rpn += char
        elif char == '*':
            while stack and stack[-1] != '(':
                rpn += stack.pop()
            stack.append(char)
        elif char == '+':
            while part1 and stack and stack[-1] != '(':
                rpn += stack.pop()
            stack.append(char)
        elif char == '(':
            # We'll deal with this when we find the closing paren
            stack.append(char)
        elif char == ')':
            c = stack.pop()
            while c != '(':
                rpn += c
                c = stack.pop()

    while stack:
        rpn += stack.pop()
    return rpn

def evaluate(rpn):
    operators = {'+', '*'}
    stack = []
    for char in rpn:
        if char.isnumeric():
            stack.append(char)
        elif char in operators:
            left, right = int(stack.pop()), int(stack.pop())
            val = left + right if char == '+' else left * right
            # print('{} {} {} = {}'.format(left, char, right, val))
            stack.append(val)
    return stack.pop()

with open(sys.argv[1], 'rt') as f:
    lines = [f.strip().replace(' ', '') for f in f.readlines()]

# Part 1
exprs = [parse(l, part1=True) for l in lines]
results = [evaluate(expr) for expr in exprs]
print(f'Part 1: {sum(results)}')

# Part 2
exprs = [parse(l) for l in lines]
results = [evaluate(expr) for expr in exprs]
print(f'Part 2: {sum(results)}')
