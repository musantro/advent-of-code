from copy import deepcopy
from functools import cache
from itertools import chain, combinations_with_replacement, zip_longest
from unittest import TestCase


def get_data(input: str):
    lines = input.split("\n")

    for line in lines:
        records, raw_sequences = line.split()
        clues = tuple(map(int, raw_sequences.split(",")))
        yield (records, clues)


def possible_arrangements(input: str, unfoldable=False) -> int:
    if unfoldable:
        return sum(num_valid_arrangements(*unfold(*data)) for data in get_data(input))
    else:
        return sum(num_valid_arrangements(*data) for data in get_data(input))


@cache
def num_valid_arrangements(springs, clues, run_size=0):
    if not springs:
        if (len(clues) == 1 and clues[0] == run_size) or (
            len(clues) == 0 and run_size == 0
        ):
            return 1
        return 0
    spring = springs[0]
    springs = springs[1:]
    clue, *new_clues = clues or [0]
    new_clues = tuple(new_clues)
    if spring == "?":
        return num_valid_arrangements(
            "#" + springs, clues, run_size
        ) + num_valid_arrangements("." + springs, clues, run_size)
    if spring == "#":
        return (
            0
            if run_size > clue
            else num_valid_arrangements(springs, clues, run_size + 1)
        )
    if spring == ".":
        if run_size == 0:
            return num_valid_arrangements(springs, clues, 0)
        if run_size == clue:
            return num_valid_arrangements(springs, new_clues, 0)
        return 0
    raise ValueError("Spring not one of #.?")


def unfold(springs, clues):
    return "?".join([springs] * 5), clues * 5


class AdventTest(TestCase):
    examples = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

    def test_first_case(self):
        results = [1, 4, 1, 1, 4, 10]

        for line, result in zip(self.examples.split("\n"), results):
            self.assertEqual(possible_arrangements(line), result, line)

        self.assertEqual(
            sum(
                possible_arrangements(sequence)
                for sequence in self.examples.split("\n")
            ),
            21,
        )

    def test_second_case(self):
        results = [1, 16384, 1, 16, 2500, 506250]
        
        for line, result in zip(self.examples.split("\n"), results):
            self.assertEqual(possible_arrangements(line, unfoldable=True), result, line)

        self.assertEqual(
            sum(
                possible_arrangements(sequence, unfoldable=True)
                for sequence in self.examples.split("\n")
            ),
            525152,
        )


if __name__ == "__main__":
    with open("advent/2023/input_2023_12.txt", "r") as f:
        text = f.read()

        result = sum(possible_arrangements(sequence) for sequence in text.split("\n"))

        print(f"2023 Day 12: Part 1: {result=}")

        result = sum(possible_arrangements(sequence, unfoldable=True) for sequence in text.split("\n"))

        print(f"2023 Day 12: Part 2: {result=}")        