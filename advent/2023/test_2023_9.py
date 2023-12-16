from unittest import TestCase


def get_next_value_int(sequence: list[int]) -> int:
    if len(set(sequence)) == 1:
        return sequence[0]
    else:
        return sequence[-1] + get_next_value_int(
            [y - x for x, y in zip(sequence[:-1], sequence[1:])]
        )


def get_prev_value_int(sequence: list[int]) -> int:
    if len(set(sequence)) == 1:
        return sequence[0]
    else:
        return sequence[0] - get_prev_value_int(
            [y - x for x, y in zip(sequence[:-1], sequence[1:])]
        )


def get_next_value(sequence: str) -> int:
    return get_next_value_int([int(num) for num in sequence.split()])


def get_prev_value(sequence: str) -> int:
    return get_prev_value_int([int(num) for num in sequence.split()])


class AdventTest(TestCase):
    def test_first_case(self):
        example = "0 3 6 9 12 15"

        self.assertEqual(get_next_value(example), 18)

    def test_second_case(self):
        example = "1 3 6 10 15 21"
        self.assertEqual(get_next_value(example), 28)

    def test_third_case(self):
        example = "10 13 16 21 30 45"
        self.assertEqual(get_next_value(example), 68)
        self.assertEqual(get_prev_value(example), 5)


if __name__ == "__main__":
    with open("advent/2023/input_2023_9.txt", "r") as f:
        text = f.read()
        result = sum(get_next_value(sequence) for sequence in text.split("\n"))

        print(f"2023 Day 9: Part 1: {result=}")

        result = sum(get_prev_value(sequence) for sequence in text.split("\n"))
        print(f"2023 Day 9: Part 2: {result=}")
