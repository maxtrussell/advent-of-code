"""
A little rough, but I don't have time to refine today
"""

from itertools import chain
import fileinput

def parse_input():
    numbers = []
    boards = []
    curr_board = []
    for line in fileinput.input():
        if not numbers:
            numbers = list(map(int, line.split(',')))
            continue
        if line.strip() == '':
            if curr_board:
                boards.append(curr_board)
                curr_board = []
            continue
        line = line.replace('  ', ' ')
        curr_board.append([int(x) for x in line.split(' ') if x])
    boards.append(curr_board)
    return numbers, boards

def get_possible_wins(boards):
    all_wins = []
    board_wins = {}
    for i, b in enumerate(boards):
        # Rows
        wins = [set(row) for row in b]

        # Columns
        for j in range(5):
            wins.append(set([row[j] for row in b]))

        # RIP Diagonals, lost a lot of time here :(
        # Diagonals
        # wins.append({b[i][i] for i in range(5)})
        # wins.append({b[i][4-i] for i in range(5)})
        board_wins[i] = wins
        all_wins.extend(wins)
    return all_wins, board_wins

def get_winning_combos(all_wins, played):
    winning_combos = []
    for win in all_wins:
        if len(win - set(played)) == 0:
            winning_combos.append(win)
    return winning_combos

def find_winning_boards(winning_combos, board_wins):
    winning_boards = set()
    for combo in winning_combos:
        for board, wins in board_wins.items():
            if combo in wins:
                winning_boards.add(board)
                break
    return winning_boards

def play_until_wins(nums, all_wins, board_wins, wins):
    played = []
    winning_combos = []
    winning_boards = []
    for n in nums:
        played.append(n)
        winning_combos = get_winning_combos(all_wins, played)
        if winning_combos:
            winning_boards.extend([
                board for board in
                find_winning_boards(winning_combos, board_wins)
                if board not in winning_boards
            ])
            winning_combos = []
        if len(winning_boards) >= wins:
            break
    return winning_boards, played

def calculate_score(board, played):
    scoring_tiles = [x for x in chain(*board) if x not in played]
    return sum(scoring_tiles) * played[-1]

numbers, boards = parse_input()
all_wins, board_wins = get_possible_wins(boards)
winners, played = play_until_wins(numbers, all_wins, board_wins, 1)
print(calculate_score(boards[winners[0]], played))
winners, played = play_until_wins(numbers, all_wins, board_wins, len(boards))
print(calculate_score(boards[winners[-1]], played))
