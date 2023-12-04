import lib.aoc as aoc

def get_winning_nums(line: str) -> int:
    winners, have = [{int(x) for x in str.split(' ') if x}
                     for str in line.split(': ')[1].split(' | ')]
    return len(winners & have)

part1 = 0
num_cards = [1 for _ in aoc.input_lines()]
for i, winning_nums in enumerate(map(get_winning_nums, aoc.input_lines())):
    if winning_nums > 0:
        part1 += 2 ** (winning_nums - 1)
        for j in range(winning_nums):
            num_cards[i + j + 1] += num_cards[i]

aoc.output(part1)
aoc.output(sum(num_cards))
