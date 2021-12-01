import fileinput

my_input = list(map(int, fileinput.input()))
count_increases = lambda nums, window_size: sum(y > x for x,y in zip(nums, nums[window_size:]))
print(f'Part 1: {count_increases(my_input, 1)}')
print(f'Part 2: {count_increases(my_input, 3)}')
