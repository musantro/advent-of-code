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

    return {end: (start, [el for el in iterate_through_numbers(numbers)])}


def iterate_through_numbers(numbers: str):
    for line in numbers.split("\n"):
        start, end, qty = line.split(" ")
        yield int(start), int(end), int(qty)


def query_almanac(
    almanac: dict[str, tuple[str, list[tuple[int, int, int]]]], source: str, number: int
):
    match almanac[source]:
        case (destination, mapping) if destination == "seed":
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

    location = 0

    while True:
        if location % 1000000 == 0:
            print(f"{location=}")
        seed = query_almanac(almanac, "location", location)
        if seed in seeds:
            return location
        location += 1


def get_lowest_location_number_by_range_seeds(text: str) -> int:
    seeds, almanac = extract_almanac(text)

    location = 0

    seeds = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]

    while True:
        if location % 1000000 == 0:
            print(f"{location=}")
        virtual_seed = query_almanac(almanac, "location", location)
        for first_seed, range_seed in seeds:
            if first_seed <= virtual_seed <= first_seed + range_seed - 1:
                return location
        location += 1


class AdventTest(TestCase):
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

    def test_part_2(self):
        result = get_lowest_location_number_by_range_seeds(self.example)

        self.assertEqual(result, 46)


if __name__ == "__main__":

    with open("advent/2023/input_2023_5.txt", "r") as f:
        text = f.read()
        result = get_lowest_location_number_by_range_seeds(text)

        print(f"2023 Day 5: Part 2: {result=}")
