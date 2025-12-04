import lib.aoc as aoc


def get_largest_n(row, n):
    if n == 0:
        return ""
    choice = max(row[: len(row) - n + 1])
    return choice + get_largest_n(row[row.index(choice) + 1 :], n - 1)


print(sum(int(get_largest_n(l, 2)) for l in aoc.input_lines()))
print(sum(int(get_largest_n(l, 12)) for l in aoc.input_lines()))
