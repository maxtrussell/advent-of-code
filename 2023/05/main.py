import lib.aoc as aoc

# (start, end, delta)
Range = tuple[int, int, int]
Map = list[Range]

# (start, end)
Pair = tuple[int, int]

def translate(m: Map, pairs: list[Pair]) -> list[Pair]:
    output = []
    for start, end in pairs:
        for r_start, r_end, delta in m:
            # Add the left-most split, no delta because it is outside the range.
            output.append((start, min(r_start, end)))

            # Add the parts of the pair inside the range, translated by delta.
            output.append((max(start, r_start) + delta, min(end, r_end) + delta))

            # We don't need to re-tread ground, advance the cursor.
            start = max(start, min(r_end, end))
        output.append((start, end))
    return output

def solve(maps: list[Map], seeds: list[Pair]):
    for m in maps:
        seeds = [(a, b) for a, b in translate(m, seeds) if a < b]
    return min(a for a, _ in seeds)

def parse_maps() -> list[Map]:
    maps = []
    current_map = []
    for i, line in enumerate(aoc.input_lines()):
        if i == 0: continue
        if not line and current_map:
            maps.append(current_map)
            current_map = []
        if not line or not line[0].isdigit(): continue

        dst, src, size = [int(x) for x in line.split(' ')]
        current_map.append((src, src+size, dst-src))
    maps.append(current_map)
    return [sorted(m) for m in maps]

seeds = [int(x) for x in aoc.input_lines()[0].split(':')[1].split()]
maps = parse_maps()

part1 = solve(maps, [(x, x+1) for x in seeds])
part2 = solve(maps, [(x, x+y) for x, y in zip(seeds[::2], seeds[1::2])])
aoc.output(part1)
aoc.output(part2)
