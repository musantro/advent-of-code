from unittest import TestCase

puzzle_input_url = "https://adventofcode.com/2015/day/1/input"


def get_floor(directions: str) -> int:
    floor = 0
    for direction in directions:
        match direction:
            case "(":
                floor += 1
            case ")":
                floor -= 1

    return floor


def get_when_gets_basement(directions: str) -> int:
    floor = 0
    index = 0
    for direction in directions:
        index += 1
        match direction:
            case "(":
                floor += 1
            case ")":
                floor -= 1
            case unknown_char:
                raise Exception(f"Not expected to get \"{unknown_char}\"")

        if floor < 0:
            return index
        
    return index


class AdventTest(TestCase):
    def test_part_1(self):
        examples = [
            ("(())", 0),
            ("()()", 0),
            ("(((", 3),
            ("(()(()(", 3),
            ("))(((((", 3),
            ("())", -1),
            ("))(", -1),
            (")))", -3),
            (")())())", -3),
        ]

        for example, solution in examples:
            self.assertEqual(get_floor(example), solution, example)


if __name__ == "__main__":
    with open("advent/2015/input_2015_1.txt", "r") as f:
        result = get_floor(f.read())
    print(f"2015 Day 1 Part 1: {result=}")

    with open("advent/2015/input_2015_1.txt", "r") as f:
        result = get_when_gets_basement(f.read())

    print(f"2015 Day 1 Part 2: {result=}")
