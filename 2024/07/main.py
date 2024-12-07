import lib.aoc as aoc
from operator import add, mul
from typing import Callable


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def parse_eq(line: str) -> tuple[int, list[int]]:
    ans, nums = line.split(": ")
    return int(ans), [int(x) for x in nums.split(" ")]


def eval_eq(
    ans: int, nums: list[int], i: int, val: int, ops: list[Callable[[int, int], int]]
) -> bool:
    if i == len(nums):
        return val == ans
    return any(eval_eq(ans, nums, i + 1, op(val, nums[i]), ops) for op in ops)


p1, p2 = 0, 0
for line in aoc.input_lines():
    ans, nums = parse_eq(line)
    if eval_eq(ans, nums, 1, nums[0], [add, mul]):
        p1 += ans
    if eval_eq(ans, nums, 1, nums[0], [add, mul, concat]):
        p2 += ans


aoc.output(p1)
aoc.output(p2)
