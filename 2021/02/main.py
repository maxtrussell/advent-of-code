import fileinput

my_input = [x.strip().split(' ') for x in fileinput.input()]

x, y = 0, 0
for cmd, magnitude in my_input:
    magnitude = int(magnitude)
    if cmd == 'forward':
        x += magnitude
    elif cmd == 'down':
        y += magnitude
    else:
        y -= magnitude
print(x * y)


aim, x, y = 0, 0, 0
for cmd, magnitude in my_input:
    magnitude = int(magnitude)
    if cmd == 'forward':
        x += magnitude
        y += magnitude * aim
    elif cmd == 'down':
        aim += magnitude
    else:
        aim -= magnitude
print(x * y)
