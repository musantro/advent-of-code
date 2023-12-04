from collections import Counter
from functools import reduce
from unittest import TestCase


def extract_cards(text: str) -> list[tuple[list[int], ...]]:
    raw_cards = [card for card in text.split("\n")]
    cards = [card.split(":").pop() for card in raw_cards]
    return [
        tuple(
            [
                [int(num.strip()) for num in game.split(" ") if num.isnumeric()]
                for game in card.split("|")
            ]
        )
        for card in cards
    ]


def get_points(text: str) -> list[int]:
    cards = extract_cards(text)

    return [
        reduce(
            (lambda x, y: x * 2 if x != 0 else 1),
            [num for num in own_numbers if num in winning_numbers],
            0,
        )
        for winning_numbers, own_numbers in cards
    ]


def get_scratchcards(text: str) -> Counter:
    scratchcards = Counter()
    cards = extract_cards(text)
    for game_num, (winning_numbers, own_numbers) in enumerate(cards, 1):
        scratchcards.update({game_num: 1})
        instances =  (scratchcards.get(game_num, 0))
        wins = len([num for num in own_numbers if num in winning_numbers])
        next_game = game_num + 1
        scratchcards.update({k: instances for k in range(next_game, next_game + wins)})
    return scratchcards


class AdventTest(TestCase):
    def test_part_1(self):
        example = (
            "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n"
            "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\n"
            "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\n"
            "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\n"
            "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\n"
            "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
        )

        numbers = get_points(example)

        self.assertEqual(sum(numbers), 13)

    def test_part_2(self):
        example = (
            "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n"
            "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\n"
            "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\n"
            "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\n"
            "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\n"
            "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
        )

        scratchcards = get_scratchcards(example)

        self.assertEqual(scratchcards.total(), 30)


if __name__ == "__main__":
    with open("advent/2023/input_2023_4.txt", "r") as f:
        text = f.read()
        numbers = get_points(text)
        result = sum(numbers)

        print(f"2023 Day 4: Part 1: {result=}")

    with open("advent/2023/input_2023_4.txt", "r") as f:
        text = f.read()
        scratchcards = get_scratchcards(text)
        result = scratchcards.total()

        print(f"2023 Day 4: Part 1: {result=}")
