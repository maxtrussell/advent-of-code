import lib.aoc as aoc

from collections import Counter
from dataclasses import dataclass
from functools import cached_property

def categorize_hand(hand: list[int]):
    hand_type = 0
    jokers = hand.count(1)

    # 4 jokers will always be able to get 5 of a kind.
    if jokers >= 4: return 6
    # 3 jokers with a pair will get 5 of a kind, otherwise 4 of a kind.
    if jokers == 3:
        if is_n_of_a_kind(hand, 2):
            return 6
        return 5
    
    if jokers == 0:
        if is_n_of_a_kind(hand, 5): hand_type = 6    # 5 of a kind
        elif is_n_of_a_kind(hand, 4): hand_type = 5  # 4 of a kind
        elif is_full_house(hand): hand_type = 4      # full house
        elif is_n_of_a_kind(hand, 3): hand_type = 3  # 3 of a kind
        elif is_two_pair(hand): hand_type = 2        # two pair
        elif is_n_of_a_kind(hand, 2): hand_type = 1  # one pair
        return hand_type

    for i, x in enumerate(hand):
        if x != 1: continue
        for y in range(2, 15):
            hand[i] = y
            hand_type = max(hand_type, categorize_hand(hand))
            hand[i] = 1
    return hand_type

@dataclass
class Hand:
    hand: list[int]
    bet: int

    @cached_property
    def score(self):
        hand_type = categorize_hand(self.hand)
        return int(str(hand_type) + ''.join([f'{x:02}' for x in self.hand]))

    def jacks_to_jokers(self):
        return Hand([x if x != 11 else 1 for x in self.hand], self.bet)
        
face_cards = {
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

def normalize(x):
    if x in face_cards:
        return face_cards[x]
    return x

def is_n_of_a_kind(hand, n):
    return any(x == n for x in Counter(hand).values())

def is_full_house(hand):
    return is_n_of_a_kind(hand, 3) and is_n_of_a_kind(hand, 2)

def is_two_pair(hand):
    return len([True for x in Counter(hand).values() if x == 2]) == 2
    
# Tuple(hand, bet)
hands = []
for line in aoc.input_lines():
    h, b = line.split()
    hands.append(Hand(hand=[int(normalize(x)) for x in h], bet=int(b)))

part1 = 0
hands.sort(key=lambda x: x.score)
for i, hand in enumerate(hands, start = 1):
    part1 += i * hand.bet
    hands[i-1] = hand.jacks_to_jokers()

part2 = 0
hands.sort(key=lambda x: x.score)
for i, hand in enumerate(hands, start = 1):
    part2 += i * hand.bet

aoc.output(part1)
aoc.output(part2)
