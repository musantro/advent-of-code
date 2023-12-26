from decimal import *
import itertools
from unittest import TestCase

getcontext().prec = 50

example = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""


class Line:
    def __init__(self, m: Decimal, n: Decimal) -> None:
        self.m = m
        self.n = n

    @classmethod
    def from_regex(cls, input: str):
        point, vel = input.split("@")

        [x, y, z] = map(Decimal, (point).split(","))
        [vx, vy, vz] = map(Decimal, (vel).split(","))

        m = vy / vx

        b = y - m * x

        cls.initial_point = (x, y, z)
        cls.velocity = (vx, vy, vz)

        return cls(vy / vx, b)


def paths_crossed(
    l1: Line, l2: Line, min: tuple[float, float], max: tuple[float, float]
) -> bool:
    try:
        x = (l1.n - l2.n) / (l2.m - l1.m)
        y = l1.m * x + l1.n
    except ZeroDivisionError:
        return False
    else:
        min_x, min_y = min
        max_x, max_y = max
        x1, y1, _ = l1.initial_point
        x2, y2, _ = l2.initial_point
        vx1, vy1, _ = l1.velocity
        vx2, vy2, _ = l2.velocity

        return all(
            [
                x > min_x,
                y > min_y,
                x < max_x,
                y < max_y,
                (x1 - x) * vx1 > Decimal(0),
                (x2 - x) * vx2 > Decimal(0),
                (y1 - y) * vy1 > Decimal(0),
                (y2 - y) * vy2 > Decimal(0),
            ]
        )


def part_1(input: str, start, end) -> int:
    lines = [Line.from_regex(line) for line in input.split("\n")]

    return sum(
        [
            paths_crossed(l1, l2, start, end)
            for (l1, l2) in itertools.combinations(lines, 2)
        ]
    )


class AdventTest(TestCase):
    def test_paths(self):
        self.assertEqual(part_1(example, (Decimal(7), Decimal(7)), (Decimal(27), Decimal(27))), 2)


if __name__ == "__main__":
    with open("advent/2023/input_2023_24.txt") as input:
        print(
            part_1(
                input.read(),
                (Decimal(200000000000000), Decimal(200000000000000)),
                (Decimal(400000000000000), Decimal(400000000000000)),
            )
        )
