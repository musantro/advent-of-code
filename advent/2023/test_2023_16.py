from unittest import TestCase

EMPTY = "."
HSPLIT = "-"
VSPLIT = "|"
FORWARD_MIRROR = "/"
BACKWARD_MIRROR = "\\"


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


example = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


class Game:
    def __init__(self, layout: str) -> None:
        self.layout = layout.split("\n")
        self.width = len(self.layout[0])
        self.height = len(self.layout)

    def neighbour(self, x: int, y: int, dir):
        if dir == NORTH and y > 0:
            return (x, y - 1, dir)
        elif dir == EAST and x + 1 < self.width:
            return (x + 1, y, dir)
        elif dir == SOUTH and y + 1 < self.height:
            return (x, y + 1, dir)
        elif dir == WEST and x > 0:
            return (x - 1, y, dir)

    def next_tiles(self, x: int, y: int, tile: str, dir):
        if tile == EMPTY:
            if nb := self.neighbour(x, y, dir):
                yield nb
        elif tile == BACKWARD_MIRROR:
            to = {NORTH: WEST, EAST: SOUTH, SOUTH: EAST, WEST: NORTH}[dir]
            if nb := self.neighbour(x, y, to):
                yield nb
        elif tile == FORWARD_MIRROR:
            to = {NORTH: EAST, EAST: NORTH, SOUTH: WEST, WEST: SOUTH}[dir]
            if nb := self.neighbour(x, y, to):
                yield nb
        elif tile == HSPLIT:
            if dir in [EAST, WEST]:
                if nb := self.neighbour(x, y, dir):
                    yield nb
            else:
                if nb := self.neighbour(x, y, EAST):
                    yield nb
                if nb := self.neighbour(x, y, WEST):
                    yield nb
        elif tile == VSPLIT:
            if dir in [NORTH, SOUTH]:
                if nb := self.neighbour(x, y, dir):
                    yield nb
            else:
                if nb := self.neighbour(x, y, NORTH):
                    yield nb
                if nb := self.neighbour(x, y, SOUTH):
                    yield nb

    def trace_beam(self, init_x: int, init_y: int, init_dir) -> int:
        history = set()

        beams = [(init_x, init_y, init_dir)]
        while beams:
            x, y, dir = beams.pop()

            if (
                (x, y, dir) not in history
                and 0 <= x < self.width
                and 0 <= y < self.height
            ):
                history.add((x, y, dir))
                beams.extend(self.next_tiles(x, y, self.layout[y][x], dir))

        return len(set((x, y) for x, y, _ in history))

    def get_best_trace_beam(self) -> int:
        best = 0
        for x in range(self.width):
            best = max(best, self.trace_beam(x, 0, SOUTH))
            best = max(best, self.trace_beam(x, self.height - 1, NORTH))
        for y in range(self.height):
            best = max(best, self.trace_beam(0, y, EAST))
            best = max(best, self.trace_beam(self.width - 1, y, WEST))

        return best


class AdventTest(TestCase):
    game = Game(example)

    def test_part_1(self):
        self.assertEqual(self.game.trace_beam(0, 0, EAST), 46)

    def test_part_2(self):
        self.assertEqual(self.game.get_best_trace_beam(), 51)


if __name__ == "__main__":
    with open("advent/2023/input_2023_16.txt", "r") as f:
        layout = f.read()

    game = Game(layout)

    print(f"2023 Day 16: Part 1: {game.trace_beam(0,0,EAST)}")
    print(f"2023 Day 16: Part 2: {game.get_best_trace_beam()}")
