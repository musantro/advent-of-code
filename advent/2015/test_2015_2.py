from functools import reduce
from unittest import TestCase

puzzle_input_url = "https://adventofcode.com/2015/day/1/input"


def get_square_feet_of_wrapping_paper(raw_dimensions: str) -> int:
    dimensions = [int(number) for number in raw_dimensions.split("x")]
    l, w, h = dimensions
    smallest_dimension = min([l*w, w*h, h*l])

    return 2 * (l*w + w*h + h*l) + smallest_dimension

def get_feet_of_ribbon(raw_dimensions: str) -> int:
    dimensions = [int(number) for number in raw_dimensions.split("x")]

    return sum(list(sorted(dimensions))[:2]) * 2 + reduce((lambda x, y: x * y), dimensions)


class AdventTest(TestCase):
    def test_part_1(self):
        examples = [
            ("2x3x4", 58),
            ("1x1x10", 43),
        ]

        for example, solution in examples:
            self.assertEqual(
                get_square_feet_of_wrapping_paper(example), solution, example
            )

    def test_part_2(self):
        examples = [
            ("2x3x4", 34),
            ("1x1x10", 14),
        ]

        for example, solution in examples:
            self.assertEqual(get_feet_of_ribbon(example), solution, example)


if __name__ == "__main__":
    with open("advent/2015/input_2015_2.txt", "r") as f:
        result = 0

        for input_line in f:
            input_line = input_line.rstrip()
            sq_ft_paper_gift = get_square_feet_of_wrapping_paper(input_line)
            result += sq_ft_paper_gift
        
    print(f"2015 Day 1 Part 1: {result=}")

    with open("advent/2015/input_2015_2.txt", "r") as f:
        result = 0

        for input_line in f:
            input_line = input_line.rstrip()
            sq_ft_paper_gift = get_feet_of_ribbon(input_line)
            result += sq_ft_paper_gift
        
    print(f"2015 Day 1 Part 2: {result=}")
