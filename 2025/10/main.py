import lib.aoc as aoc

from collections import deque
import re
import z3


class Machine:
    def __init__(self, lights, buttons, joltages):
        self.lights = [0 if x == "." else 1 for x in lights]
        self.buttons = buttons
        self.joltages = joltages

    def configure_lights(self):
        """BFS to find minimum presses."""
        q = deque()
        q.append((0, [0 for _ in self.lights]))
        seen = set()
        while True:
            presses, lights = q.popleft()
            if lights == self.lights:
                return presses
            if tuple(lights) in seen:
                continue
            seen.add(tuple(lights))

            for button in self.buttons:
                new_lights = [x ^ int(i in button) for i, x in enumerate(lights)]
                q.append((presses + 1, new_lights))

    def configure_joltages(self):
        """BFS was too slow, use z3 solver instead."""
        opt = z3.Optimize()
        press_counts = [z3.Int(f"press_{i}") for i in range(len(self.buttons))]

        # Presses cannot be negative.
        opt.add(z3.And([p >= 0 for p in press_counts]))

        # Joltage requirements must be met.
        for i in range(len(self.joltages)):
            opt.add(
                sum(press_counts[j] for j, b in enumerate(self.buttons) if i in b)
                == self.joltages[i]
            )

        # Minimize presses.
        opt.minimize(sum(press_counts))
        opt.check()

        model = opt.model()
        return sum(model[p].as_long() for p in press_counts)


machines = []
for line in aoc.input_lines():
    match = re.search(r"\[([\.#]+)\]", line)
    lights = match.group(1)

    match = re.findall(r"\(([\d,]+)\)", line)
    buttons = [{int(x) for x in s.split(",")} for s in match]

    match = re.search(r"\{([\d,]+)\}", line)
    joltages = [int(x) for x in match.group(1).split(",")]

    machines.append(Machine(lights, buttons, joltages))

aoc.output(sum(m.configure_lights() for m in machines))
aoc.output(sum(m.configure_joltages() for m in machines))
