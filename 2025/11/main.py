import lib.aoc as aoc

from functools import cache

graph = {}


@cache
def dfs(dev, dac, fft):
    if dev == "out":
        return int(dac and fft)
    dac |= dev == "dac"
    fft |= dev == "fft"
    return sum(dfs(c, dac, fft) for c in graph[dev])


for line in aoc.input_lines():
    dev, connections = line.split(":")
    graph[dev] = connections.split()

aoc.output(dfs("you", True, True))
aoc.output(dfs("svr", False, False))
