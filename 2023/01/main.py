import lib.aoc as aoc
import typing as t

spelled = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}
reverse_spelled = {k[::-1]:v for k, v in spelled.items()}

def get_value(line: str, i: int, spelled={}) -> t.Optional[str]:
    if line[i].isdigit():
        return line[i]

    # The longest spelling is of length 5.
    for j in range(6):
        if line[i:i+j] in spelled:
            return str(spelled[line[i:i+j]])

def get_calibrated_values(forward: dict[str, int] = {}, backward: dict[str, int] = {}) -> int:
    calibrated_values = []
    for line in aoc.input_lines():
        left = right = ''

        # Probe forward for a number
        for i in range(len(line)):
            left = get_value(line, i, forward)
            if left: break

        # Probe backward for a number
        rev = line[::-1]
        for i in range(len(rev)):
            right = get_value(rev, i, backward)
            if right: break

        calibrated_values.append(int(left + right))
    return sum(calibrated_values)

print(f'Part 1: {get_calibrated_values()}')
print(f'Part 2: {get_calibrated_values(spelled, reverse_spelled)}')
