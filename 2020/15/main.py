import collections

def memory_game(starting_numbers, last_turn):
    turns = collections.defaultdict(list)
    turn = 1
    for num in starting_numbers:
        turns[num] = [turn]
        turn += 1

    last_num = starting_numbers[-1]
    while turn <= last_turn:
        if len(turns[last_num]) > 1:
            new_num = turns[last_num][-1] - turns[last_num][-2]
        else:
            new_num = 0

        turns[new_num].append(turn)
        last_num = new_num
        turn += 1
    return last_num

print(memory_game([16,12,1,0,15,7,11], 2020))
print(memory_game([16,12,1,0,15,7,11], 30000000))
