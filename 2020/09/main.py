

def first_invalid(sequence):
    for i in range(25, len(sequence)):
        if not two_sum(sequence[i-25:i], sequence[i]):
            return sequence[i]
    return None

# Copied from day 1
def two_sum(data, target):
    diffs = set()
    for entry in data:
        diff = target - entry
        if diff in diffs:
            return True
        diffs.add(entry)
    return False

# This would be O(n) with a partial sum, but it's fast enough as is
def contiguous_sum(sequence, target):
    for i in range(len(sequence)):
        rolling_sum = 0
        j = i
        while rolling_sum < target:
            rolling_sum += sequence[j]
            j += 1

        if rolling_sum == target:
            return min(sequence[i:j]) + max(sequence[i:j])
    return None

with open('input.txt', 'rt') as f:
    sequence = [int(l) for l in f.readlines()]

# Part 1
invalid = first_invalid(sequence)
print(f'Part 1: {invalid}')

# Part 2
weakness = contiguous_sum(sequence, invalid)
print(f'Part 2: {weakness}')
