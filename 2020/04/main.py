import re
import typing as t

def read_input(path: str) -> t.List[t.Dict[str, str]]:
    passports = []
    with open(path, 'rt') as f:
        for passport in f.read().split('\n\n'):
            passports.append(parse_passport(passport))
    return passports

def parse_passport(line: str) -> t.Dict[str, str]:
    return {k:v for k,v in [p.strip().split(':') for p in re.split(' |\n', line) if p.strip()]}

def is_valid_part1(passport: t.Dict[str, str], req: t.List[str]) -> bool:
    return all([field in passport for field in req])

def is_valid_part2(
    passport: t.Dict[str, str],
    req: t.Dict[str, t.Callable[[str, str], bool]],
) -> bool:
    for key, is_valid in req.items():
        if key not in passport or not is_valid(key, passport[key]):
            return False
    return True

def validate_year(key: str, val: str) -> bool:
    bounds = {
        'byr': (1920, 2002),
        'iyr': (2010, 2020),
        'eyr': (2020, 2030),
    }
    min, max = bounds.get(key, (-1, -1))
    return min <= int(val) <= max

def validate_height(_: str, val: str) -> bool:
    if val.endswith('cm'):
        min, max = 150, 193
    elif val.endswith('in'):
        min, max = 59, 76
    else:
        return False
    height = int(val[:-2])
    return min <= height <= max

req = {
    # All validation functions are of type func(str, str) -> bool
    'byr': validate_year,
    'iyr': validate_year,
    'eyr': validate_year,
    'hgt': validate_height,
    'hcl': lambda _, val: re.match('#[a-f0-9]{6}', val) is not None,
    'ecl': lambda _, val: val in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
    'pid': lambda _, val: len(val) == 9,
}
passports = read_input('input.txt')

# Part 1
valid = [p for p in passports if is_valid_part1(p, req.keys())]
print(f'Part 1: {len(valid)}')

# Part 2
valid = [p for p in valid if is_valid_part2(p, req)]
print(f'Part 2: {len(valid)}')
