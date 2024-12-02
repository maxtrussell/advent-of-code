import lib.aoc as aoc


def is_safe(report) -> bool:
    diffs = []
    for l, r in zip(report, report[1:]):
        diffs.append(l - r)
        if abs(diffs[-1]) < 1 or abs(diffs[-1]) > 3:
            return False
    increasing = sum(x > 0 for x in diffs)
    return increasing == 0 or increasing == len(diffs)


def get_variants(report):
    for i in range(0, len(report)):
        yield report[:i] + report[i + 1 :]


p1, p2 = 0, 0
for line in aoc.input_lines():
    report = [int(x) for x in line.split(" ")]
    p1 += is_safe(report)
    p2 += any(is_safe(v) for v in get_variants(report))

aoc.output(p1)
aoc.output(p2)
