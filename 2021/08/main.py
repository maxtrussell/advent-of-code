import fileinput
import itertools

digits = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9,
}

def translate(s, mapping):
    return ''.join(sorted(mapping[x] for x in s))

def decode(patterns, output):
    # Brute force :)
    for perm in itertools.permutations('abcdefg'):
        mapping = {x:y for x,y in zip(perm, 'abcdefg')}

        # Using a generator instead of a list for translated patterns
        # cut runtime in 1/4 This is because patterns are no longer
        # translated after the first invalid translation.
        translated_patterns = map(lambda x: translate(x, mapping), patterns)
        if all((x in digits) for x in translated_patterns):
            output = [digits[translate(x, mapping)] for x in output]
            return int(''.join(map(str, output)))
    raise Exception(f'Pattern not decoded: {patterns}')

patterns = []
outputs = []
for line in fileinput.input():
    line = line.strip()
    pattern, output = line.split(' | ')
    patterns.append(pattern.split(' '))
    outputs.append(output.split(' '))

cnt = 0
for pattern, output in zip(patterns, outputs):
    cnt += len([x for x in output if len(x) in [2, 4, 3, 7]])
print(cnt)

print(sum([decode(p, o) for p,o in zip(patterns, outputs)]))
