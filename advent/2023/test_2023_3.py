from functools import reduce
from typing import Tuple
from unittest import TestCase
from venv import create


def get_neighbors(i, j):
    start_i = max(i - 1, 0)
    end_i = i + 1
    start_j = max(j - 1, 0)
    end_j = j + 1

    for x in range(start_i, end_i + 1):
        for y in range(start_j, end_j + 1):
            if not (x, y) == (i, j):
                yield x, y


def create_matrix(input: str) -> list[str]:
    return input.split("\n")


def is_symbol(char: str) -> bool:
    match char:
        case ".":
            return False
        case c if c.isnumeric():
            return False
        case _:
            return True


def is_gear(char: str) -> bool:
    match char:
        case "*":
            return True
        case _:
            return False


def get_symbols(matrix: list[str]) -> list[tuple[int, int]]:
    return [
        (i, j)
        for i, line in enumerate(matrix)
        for j, char in enumerate(line)
        if is_symbol(char)
    ]


def get_gears(matrix: list[str]) -> list[tuple[int, int]]:
    return [
        (i, j)
        for i, line in enumerate(matrix)
        for j, char in enumerate(line)
        if is_gear(char)
    ]


def extract_number(matrix: list[str], pair: tuple[int, int]) -> None | tuple[int, int]:
    i, j = pair
    try:
        if not matrix[i][j].isnumeric():
            return None

        line = matrix[i]

        start_idx = j
        end_idx = j
    except IndexError:
        return None

    try:
        while line[start_idx].isnumeric():
            start_idx -= 1
    except IndexError:
        pass

    try:
        while line[end_idx].isnumeric():
            end_idx += 1
    except IndexError:
        pass

    return start_idx, end_idx


def get_all_numbers_engine(raw_game_history: str):
    matrix = create_matrix(raw_game_history)

    symbols = get_symbols(matrix)

    number_indices = {
        (x, result)
        for i, j in symbols
        for x, y in get_neighbors(i, j)
        if (result := extract_number(matrix, (x, y))) is not None
    }

    return [int(matrix[i][start + 1 : end]) for (i, (start, end)) in number_indices]


def get_all_ratios(raw_game_history: str):
    matrix = create_matrix(raw_game_history)

    gears = get_gears(matrix)

    number_indices = [
        {
            (x, result)
            for x, y in get_neighbors(i, j)
            if (result := extract_number(matrix, (x, y))) is not None
        }
        for i, j in gears
    ]

    return [reduce((lambda x,y: x*y), [int(matrix[i][start + 1: end]) for (i, (start, end)) in line]) for line in number_indices if len(line) > 1]


class AdventTest(TestCase):
    def test_part_1(self):
        example = (
            "467..114..\n"
            "...*......\n"
            "..35..633.\n"
            "......#...\n"
            "617*......\n"
            ".....+.58.\n"
            "..592.....\n"
            "......755.\n"
            "...$.*....\n"
            ".664.598..\n"
        )

        numbers = get_all_numbers_engine(example)

        self.assertEqual(sum(numbers), 4361)

    def test_part_2(self):
        example = (
            "467..114..\n"
            "...*......\n"
            "..35..633.\n"
            "......#...\n"
            "617*......\n"
            ".....+.58.\n"
            "..592.....\n"
            "......755.\n"
            "...$.*....\n"
            ".664.598..\n"
        )

        numbers = get_all_ratios(example)

        self.assertEqual(sum(numbers), 467835)


if __name__ == "__main__":
    with open("advent/2023/input_2023_3.txt", "r") as f:
        text = f.read()
        numbers = get_all_numbers_engine(text)
        result = sum(numbers)

        print(f"2023 Day 3: Part 1: {result=}")

    with open("advent/2023/input_2023_3.txt", "r") as f:
        text = f.read()
        numbers = get_all_ratios(text)
        result = sum(numbers)

        print(f"2023 Day 3: Part 2: {result=}")
