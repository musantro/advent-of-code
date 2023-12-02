from functools import reduce
from typing import Tuple
from unittest import TestCase


bag = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def is_game_possible(raw_game_history: str) -> Tuple[int, bool]:
    raw_game, history = raw_game_history.split(": ")
    _, game_as_str = raw_game.split(" ")
    game_id = int(game_as_str)

    for reveals in history.split("; "):
        for reveal in reveals.split(", "):
            qty, color = reveal.split(" ")

            if bag[color] < int(qty):
                return game_id, False

    return (game_id, True)

def get_power(raw_game_history: str) -> int:
    _, history = raw_game_history.split(": ")

    minimum_bag = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }

    for reveals in history.split("; "):
        for reveal in reveals.split(", "):
            qty, color = reveal.split(" ")

            if minimum_bag[color] < int(qty):
                minimum_bag[color] = int(qty)

    
    return reduce((lambda x, y: x * y), minimum_bag.values())

    


class AdventTest(TestCase):
    def test_part_1(self):
        examples = [
            ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", True),
            ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", True),
            (
                "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
                False,
            ),
            (
                "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
                False,
            ),
            ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", True),
        ]

        result = 0

        for input_line, expected_result in examples:
            id, possible = is_game_possible(input_line)
            self.assertEqual(possible, expected_result, msg=input_line)
            if possible:
                result += id

        self.assertEqual(result, 8)

    def test_part_2(self):
        examples = [
            ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", 48),
            ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", 12),
            (
                "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
                1560,
            ),
            (
                "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
                630,
            ),
            ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", 36),
        ]

        result = 0

        for input_line, expected_result in examples:
            power = get_power(input_line)
            self.assertEqual(power, expected_result, msg=input_line)
            result += power

        self.assertEqual(result, 2286)


if __name__ == "__main__":
    with open("advent/2023/input_2023_2.txt", "r") as f:
        result = 0

        for input_line in f:
            input_line = input_line.rstrip()
            id, possible = is_game_possible(input_line)
            if possible:
                result += id

        print(f"2023 Day 2: Part 1: {result=}")


    with open("advent/2023/input_2023_2.txt", "r") as f:
        result = 0

        for input_line in f:
            input_line = input_line.rstrip()
            power = get_power(input_line)
            result += power

        print(f"2023 Day 2: Part 2: {result=}")