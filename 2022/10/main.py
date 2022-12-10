import aoc

class CPU:
    def __init__(self):
        self.X = 1  # X register
        self.cycle = 1
        self.signal = 0
        self.crt = [['.' for _ in range(40)] for _ in range(6)]
        self.milestones = (20 + 40 * x for x in range(2**10))
        self.next_milestone = next(self.milestones)

    def do_op(self, args):
        last_cycle, last_x = self.cycle, self.X
        match args[0]:
            case "addx":
                self.X += int(args[1])
                self.cycle += 2
            case "noop":
                self.cycle += 1

        # Update signal strength for part 1
        if self.cycle > self.next_milestone:
            self.signal += self.next_milestone * last_x
            self.next_milestone = next(self.milestones)

        # Update crt for part 2
        for cycle in range(last_cycle, self.cycle):
            pixel = cycle - 1
            px = pixel % 40
            py = pixel // 40
            if last_x - 1 <= px <= last_x + 1:
                self.crt[py][px] = '#'

cpu = CPU()
for line in aoc.input_lines():
    cpu.do_op(line.split(' '))
print('Part 1: ', cpu.signal)
print('Part 2:')
print('\n'.join([''.join(r) for r in cpu.crt]))
