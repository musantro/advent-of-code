from re import sub
from unittest import TestCase

alpha_numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_calibration_value(text: str) -> int:
    numbers = [character for character in text if character.isnumeric()]
    return int(str.join("", [numbers[0], numbers[-1]]))


def sum_all_calibration_values(calibration_values: list[int]) -> int:
    return sum(calibration_values)


def extract_first_number(input_str: str) -> int:
    for i in range(len(input_str)):
        if input_str[i].isnumeric():
            return int(input_str[i])
        for j in range(i + 1, len(input_str) + 1):
            if input_str[j-1].isnumeric():
                return int(input_str[j-1])
            substring = input_str[i:j]
            try:
                alpha_number = next(
                    pattern for pattern in alpha_numbers if pattern in substring
                )
                return alpha_numbers[alpha_number]
            except StopIteration:
                continue


def extract_second_number(input_str: str) -> int:

    for i in range(len(input_str)):
        for j in range(i + 1, len(input_str) + 1):
            if input_str[::-1][j-1].isnumeric():
                return int(input_str[::-1][j-1])
            substring = input_str[::-1][i:j][::-1]
            try:
                alpha_number = next(
                    pattern for pattern in alpha_numbers if pattern in substring
                )
                return alpha_numbers[alpha_number]
            except StopIteration:
                continue


def get_amended_calibration_value(text: str) -> int:
    first_number = extract_first_number(text)
    second_number = extract_second_number(text)
    return int(f"{first_number}{second_number}")


class AdventTest(TestCase):
    def test_part_1(self):
        examples = [
            ("1abc2", 12),
            ("pqr3stu8vwx", 38),
            ("a1b2c3d4e5f", 15),
            ("treb7uchet", 77),
        ]

        for input_line, expected_calibration_value in examples:
            with self.subTest(input_line, input_line=input_line):
                calibration_value = get_calibration_value(input_line)
                self.assertEqual(
                    calibration_value, expected_calibration_value, msg=input_line
                )

        calibrated_values = [
            get_calibration_value(input_line) for input_line, _ in examples
        ]
        result = sum_all_calibration_values(calibrated_values)

        self.assertEqual(result, 142, calibrated_values)

    def test_part_2(self):
        examples = [
            ("two1nine", 29),
            ("eightwothree", 83),
            ("abcone2threexyz", 13),
            ("xtwone3four", 24),
            ("4nineeightseven2", 42),
            ("zoneight234", 14),
            ("7pqrstsixteen", 76),
        ]

        for input_line, expected_calibration_value in examples:
            calibration_value = get_amended_calibration_value(input_line)
            self.assertEqual(
                calibration_value, expected_calibration_value, msg=input_line
            )
        
        
        calibrated_values = [
            get_amended_calibration_value(input_line) for input_line, _ in examples
        ]
        result = sum_all_calibration_values(calibrated_values)

        self.assertEqual(result, 281, calibrated_values)



if __name__ == "__main__":
    with open("advent/2023/input_2023_1_1.txt", "r") as f:
        calibrated_values = [
            get_calibration_value(input_line) for input_line in f.readlines()
        ]
        result = sum_all_calibration_values(calibrated_values)
        print(f"2023 Day 1: Part 1: {result=}")

    with open("advent/2023/input_2023_1_1.txt", "r") as f:
        result = 0

        for input_line in f:
            input_line = input_line.rstrip()
            calibration_value = get_amended_calibration_value(input_line)
            print(f"{calibration_value=}\t{input_line}")
            result += calibration_value
        
        print(f"2023 Day 1: Part 2: {result=}")
