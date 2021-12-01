def count_increases(nums, window_size):
    # Using a running total allows for a linear run time
    increases = 0
    prev_total = running_total = sum(nums[0:window_size])
    for i in range(window_size, len(nums)):
        # Add the new addition to the window & remove the trailing edge
        running_total += nums[i] - nums[i - window_size]
        if running_total > prev_total:
            increases += 1
        prev_total = running_total
    return increases

with open('input.txt') as f:
    my_input = [int(l.strip()) for l in f.readlines()]

print(f'Part 1: {count_increases(my_input, 1)}')
print(f'Part 2: {count_increases(my_input, 3)}')
