from collections import Counter
from unittest import TestCase

cards = []
j_as_jokers = False

def get_rank_card(card: str) -> int:
    return cards.index(card) + 1

def get_rank_hand(hand: str) -> str:
    return first_ordering_rule(hand) + second_ordering_rule(hand)

def first_ordering_rule(hand: str) -> str:
    if j_as_jokers:
        return first_ordering(substitute_joker(hand))
    else:
        return first_ordering(hand)

def first_ordering(hand: str) -> str:
    hand_explained = Counter(hand).most_common()
    match hand_explained:
        case [(full, 5), *_]:
            return "01"
        case [(four, 4), *_]:
            return "02"
        case [(a, 3), (b, 2), *_]:
            return "03"
        case [(a, 3), *_]:
            return "04"
        case [(a, 2), (b, 2), *_]:
            return "05"
        case [(a, 2), *_]:
            return "06"
        case _:
            return "07"


def second_ordering_rule(hand):
    return "".join([str(get_rank_card(card)).zfill(2) for card in hand])

def substitute_joker(hand: str) -> str:
    global cards
    possible_substitutions = list(set(hand.replace("J","")))

    possible_hands = [hand.replace("J", card) for card in possible_substitutions]

    if possible_hands:
        return min(possible_hands, key=first_ordering)
    else:
        return cards[0] * 5


def get_list_of_hands(input: str) -> list[tuple[str, int]]:
    return [(hand_and_bid.split()[0], int(hand_and_bid.split()[1])) for hand_and_bid in input.split("\n")]

def order_hands(list_of_hands: list[tuple[str, int]]) -> list[tuple[str, int]]:
    return list(sorted(list_of_hands, key=lambda hand_and_bid: get_rank_hand(hand_and_bid[0]), reverse=True))

def total_winnings(input: str) -> int:
    list_of_hands = get_list_of_hands(input)
    ordered_hands = order_hands(list_of_hands)

    return sum(bid * rank for rank, (hand, bid) in enumerate(ordered_hands, start=1))


class AdventTest(TestCase):
    def test_part_1(self):
        global cards
        cards = "AKQJT98765432"

        example = (
            "32T3K 765\n"
            "T55J5 684\n"
            "KK677 28\n"
            "KTJJT 220\n"
            "QQQJA 483"
            )
        
        self.assertEqual(total_winnings(example), 6440)
    def test_part_2(self):
        global cards, j_as_jokers
        cards = "AKQT98765432J"
        j_as_jokers = True

        example = (
            "32T3K 765\n"
            "T55J5 684\n"
            "KK677 28\n"
            "KTJJT 220\n"
            "QQQJA 483"
            )
        
        self.assertEqual(total_winnings(example), 5905)


if __name__ == "__main__":
    cards = "AKQJT98765432"

    with open("advent/2023/input_2023_7.txt", "r") as f:
        text = f.read()
        result = total_winnings(text)

        print(f"2023 Day 7: Part 1: {result=}")

    cards = "AKQT98765432J"
    j_as_jokers = True

    with open("advent/2023/input_2023_7.txt", "r") as f:
        text = f.read()
        result = total_winnings(text)

        print(f"2023 Day 7: Part 2: {result=}")    
    
