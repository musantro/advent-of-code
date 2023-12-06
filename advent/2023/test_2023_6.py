from unittest import TestCase
from functools import reduce

def get_races(text: str) -> list[tuple[int, int]]:
    time_raw, distance_raw, *_ = text.split("\n")
    return [(int(time), int(distance)) for time, distance in zip(time_raw.split()[1:], distance_raw.split()[1:])]

def run_race(button_pressed_time: int, run_time: int) -> int:
    return (run_time - button_pressed_time) * button_pressed_time

def get_records_race(race: tuple[int, int]):
    time, distance = race
    return [record for button_pressed_time in range(time) if (record := run_race(button_pressed_time, time)) > distance]

def get_records_all_races(races: list[tuple[int, int]]) -> list[int]:
    return [len(get_records_race(race)) for race in races]

def multiply_all_records(records: list[int]) -> int:
    return reduce((lambda x, y: x*y), records)

def get_result_part_1(text: str) -> int:
    races = get_races(text)
    records = get_records_all_races(races)
    return multiply_all_records(records)

def get_result_part_2(text: str) -> int:
    races = get_races(text)
    race = tuple([int(str.join("", list(map(str, t)))) for t in zip(*races)])
    records = get_records_race(race)
    return len(records)

class AdventTest(TestCase):
    example = "Time:      7  15   30\n" "Distance:  9  40  200"

    def test_get_races(self):
        expected = [(7,9),(15,40),(30,200)]
        result = get_races(self.example)
        self.assertEqual(result, expected, result)

    def test_run_race(self):
        self.assertEqual(run_race(3, 7), 12)

    def test_part_1(self):
        result = get_result_part_1(self.example)

        self.assertEqual(result, 288)

    def test_part_2(self):
        result = get_result_part_2(self.example)

        self.assertEqual(result, 71503)



if __name__ == "__main__":
    with open("advent/2023/input_2023_6.txt", "r") as f:
        text = f.read()
        result = get_result_part_1(text)

        print(f"2023 Day 6: Part 1: {result=}")

    with open("advent/2023/input_2023_6.txt", "r") as f:
        text = f.read()
        result = get_result_part_2(text)

        print(f"2023 Day 6: Part 1: {result=}")
