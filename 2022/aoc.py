from functools import cache
import os
import sys

@cache
def input_lines(strip: bool=True) -> list[str]:
    day = int(os.path.basename(os.path.dirname(sys.argv[0])))
    with open(f'{day:02}/{sys.argv[1]}', 'r') as f:
        if strip:
            return [l.strip() for l in f.readlines()]
        return f.readlines()
