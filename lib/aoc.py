from functools import cache
import os
import sys

part = 1
day = int(os.path.basename(os.path.dirname(sys.argv[0])))
year = os.path.basename(os.path.dirname(os.path.dirname(sys.argv[0])))

@cache
def input_lines(strip: bool=True) -> list[str]:
    global day
    with open(f'{year}/{day:02}/{sys.argv[1]}', 'r') as f:
        if strip:
            return [l.strip() for l in f.readlines()]
        return f.readlines()

@cache
def raw_input() -> str:
    global day
    with open(f'{day:02}/{sys.argv[1]}', 'r') as f:
        return f.read()

def output(ans):
    global part
    print(f'Part {part}: {ans}')
    part += 1
