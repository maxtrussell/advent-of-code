import fileinput

def print_dots(dots):
    y_max = max(map(lambda d: d[1], dots))
    x_max = max(map(lambda d: d[0], dots))
    for y in range(y_max+1):
        print(''.join(['#' if (x,y) in dots else '.' for x in range(x_max+1)]))

def fold(dots, value, i):
    new_dots = set()
    for dot in dots:
        if dot[i] > value:
            dot[i] -= (dot[i] - value) * 2
        new_dots.add(dot)
    return new_dots

dots = set()
folds = []
for line in map(lambda l: l.strip(), fileinput.input()):
    if not line:
        continue
    if line.startswith('fold'):
        axis, value = line.split(' ')[-1].split('=')
        folds.append((axis, int(value)))
    else:
        x, y = map(int, line.split(','))
        dots.add([x, y))

for axis, value in folds:
    dots = fold(dots.copy(), value, 0 if axis == 'x' else 1)

print_dots(dots)
