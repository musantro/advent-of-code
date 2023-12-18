from typing import Generator
from unittest import TestCase

from shapely.geometry import Point, Polygon

example = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

directions = ["R", "D", "L", "U"]


def next_point(prev_point: tuple[int, int], instruction: tuple[str, int]):
    x, y = prev_point
    match instruction:
        case ("D", qty):
            return (x, y - qty)
        case ("U", qty):
            return (x, y + qty)
        case ("L", qty):
            return (x - qty, y)
        case ("R", qty):
            return (x + qty, y)


def get_instruction(line: str, hex: bool):
    if hex:
        *_, color = line.split()
        color = color.strip("()")
        hex_meters = f"0x{color[1:-1]}"
        qty = int(hex_meters, 16)
        return directions[int(color[-1])], qty
    else:
        direction, qty, color = line.split()
        return direction, int(qty)


def get_instructions(input: str, hex: bool) -> Generator[tuple[tuple[int, int], int], None, None]:
    point = (0, 0)

    yield point, 0

    for line in input.split("\n"):
        direction, qty = get_instruction(line, hex)
        point = next_point(point, (direction, qty))
        yield point, qty


def get_area(input: str, hex: bool = False) -> int:
    points = [point for point, qty in get_instructions(input, hex)]
    edges = sum(qty for point, qty in get_instructions(input, hex))

    return calc_area(points, edges)



def calc_area(points, edges):
    """
    https://www.reddit.com/r/adventofcode/comments/18l2nk2/2023_day_18_easiest_way_to_solve_both_parts/
    https://www.reddit.com/r/adventofcode/comments/18l0qtr/comment/kdv3pvu/

    https://en.wikipedia.org/wiki/Shoelace_formula
    https://en.wikipedia.org/wiki/Pick%27s_theorem
    """
    r = 0
    for i in range(len(points) - 1):
        y1, x1 = points[i]
        y2, x2 = points[i + 1]
        r += x1 * y2 - x2 * y1
    
    return abs(r) // 2 + edges // 2 + 1


class AdventTest(TestCase):
    def test_part_1(self):
        result = [
            (0, 0),
            (6, 0),
            (6, -5),
            (4, -5),
            (4, -7),
            (6, -7),
            (6, -9),
            (1, -9),
            (1, -7),
            (0, -7),
            (0, -5),
            (2, -5),
            (2, -2),
            (0, -2),
            (0, 0),
        ]

        self.assertListEqual(
            [point for point, qty in get_instructions(example, False)], result
        )
        self.assertEqual(get_area(example), 62)
        self.assertEqual(get_area(example, True), 952408144115)


if __name__ == "__main__":
    with open("advent/2023/input_2023_18.txt", "r") as file:
        input = file.read().strip()

    print(f"2023 Day 18: Part 1: {get_area(input)}")
    print(f"2023 Day 18: Part 2: {get_area(input, True)}")
