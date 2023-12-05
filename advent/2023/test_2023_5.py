from unittest import TestCase


def extract_almanac(text: str):
    seeds, *maps = text.split("\n\n")
    seeds = [int(num) for num in seeds.replace("seeds: ", "").split(" ")]

    almanac: dict[str, tuple[str, list[tuple[int, int, int]]]] = {}

    for mapping in maps:
        almanac |= extract_maps(mapping)

    return seeds, almanac


def extract_maps(text: str) -> dict[str, tuple[str, list[tuple[int, int, int]]]]:
    mapping, numbers, *_ = text.split(" map:\n")
    start, end, *_ = mapping.split("-to-")

    return {start: (end, [el for el in iterate_through_numbers(numbers)])}

def iterate_through_numbers(numbers: str):
    for line in numbers.split("\n"):
        end, start, qty = line.split(" ")
        yield int(start), int(end), int(qty)

def query_almanac(almanac: dict[str, tuple[str, list[tuple[int, int, int]]]], source: str, number: int):
    match almanac[source]:
        case (destination, mapping) if destination == "location":
            return query_mapping(mapping, number)
        case (destination, mapping):
            return query_almanac(almanac, destination, query_mapping(mapping, number))
        
def query_mapping(mapping: list[tuple[int, int, int]], number: int) -> int:
    for source, dest, qty in mapping:
        if source <= number <= source + qty - 1:
            return dest + (number - source)
    return number

def get_lowest_location_number(text: str) -> int:
    seeds, almanac = extract_almanac(text)
    locations = [query_almanac(almanac, "seed", seed) for seed in seeds]
    return min(locations)


class AdventTest(TestCase):
    def test_part_1(self):
        example = (
            "seeds: 79 14 55 13\n"
            "\n"
            "seed-to-soil map:\n"
            "50 98 2\n"
            "52 50 48\n"
            "\n"
            "soil-to-fertilizer map:\n"
            "0 15 37\n"
            "37 52 2\n"
            "39 0 15\n"
            "\n"
            "fertilizer-to-water map:\n"
            "49 53 8\n"
            "0 11 42\n"
            "42 0 7\n"
            "57 7 4\n"
            "\n"
            "water-to-light map:\n"
            "88 18 7\n"
            "18 25 70\n"
            "\n"
            "light-to-temperature map:\n"
            "45 77 23\n"
            "81 45 19\n"
            "68 64 13\n"
            "\n"
            "temperature-to-humidity map:\n"
            "0 69 1\n"
            "1 0 69\n"
            "\n"
            "humidity-to-location map:\n"
            "60 56 37\n"
            "56 93 4"
        )

        result = get_lowest_location_number(example)

        self.assertEqual(result, 35)

if __name__ == "__main__":
    with open("advent/2023/input_2023_5.txt", "r") as f:
        text = f.read()
        result = get_lowest_location_number(text)

        print(f"2023 Day 5: Part 1: {result=}")