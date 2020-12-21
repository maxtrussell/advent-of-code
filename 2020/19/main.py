import sys

def parse_rules(lines):
    rules = {}
    for line in lines:
        num, match = line.split(": ")
        num = int(num)
        if '"' in match:
            # leaf rule
            rules[num] = match[1]
        else:
            rules[num] = [[int(r) for r in branch.split()] for branch in match.split(" | ")]
    return rules

def validate(message, rules, r):
    # leaf rule case
    if rules[r] == 'a' or rules[r] == 'b':
        return {1} if (message and message[0] == rules[r]) else set()

    # recursive rule case
    all_matches = set()
    for option in rules[r]:

        # num characters matched for current option
        option_match = {0}
        for rule in option:
            new_match = set()  # current match
            for n in option_match:
                new_match |= {n+m for m in validate(message[n:], rules, rule)}
            option_match = new_match
        all_matches |= option_match
    return all_matches

with open(sys.argv[1], 'rt') as f:
    raw_rules, messages = [part.splitlines() for part in f.read().split("\n\n")]

# Part 1
rules = parse_rules(raw_rules)
valid_messages = [m for m in messages if len(m) in validate(m, rules, 0)]
print(f'Part 1: {len(valid_messages)}')

# Part 2
rules[8] = [[42], [42, 8]]
rules[11] = [[42, 31], [42, 11, 31]]
valid_messages = [m for m in messages if len(m) in validate(m, rules, 0)]
print(f'Part 2: {len(valid_messages)}')
