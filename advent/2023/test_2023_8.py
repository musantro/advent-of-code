from typing import Generator
from unittest import TestCase


def generate_sequence(sequence: str) -> Generator[str, None, None]:
    while True:
        for element in sequence:
            yield element


def generate_nodes(
    nodes: list[str],
) -> Generator[tuple[str, tuple[str, str]], None, None]:
    for node in nodes:
        key_str, tuple_str, *_ = node.split(" = ")
        left, right, *_ = tuple(tuple_str.strip("()").split(", "))
        yield key_str, (left, right)


def parse_inputs(
    input: str,
) -> tuple[Generator[str, None, None], dict[str, tuple[str, str]]]:
    sequence, nodes, *_ = input.split("\n\n")

    return generate_sequence(sequence), {
        key: value for key, value in generate_nodes(nodes.split("\n"))
    }


def steps_to_end(input: str, current_node = "AAA", condition = lambda x: x == "ZZZ") -> int:
    sequence, nodes = parse_inputs(input)

    steps = 0

    for instruction in sequence:
        match instruction:
            case "L":
                current_node = nodes[current_node][0]
            case "R":
                current_node = nodes[current_node][1]

        steps += 1
        if condition(current_node):
            return steps
        
def steps_to_all_z(input: str) -> int | None:
    _, nodes = parse_inputs(input)

    current_nodes = [node for node in nodes.keys() if node.endswith("A")]

    import math
    return math.lcm(*[steps_to_end(input, node, lambda x: x.endswith("Z")) for node in current_nodes])
        


class AdventTest(TestCase):
    def test_part_1(self):
        example = (
            "LLR\n" "\n" "AAA = (BBB, BBB)\n" "BBB = (AAA, ZZZ)\n" "ZZZ = (ZZZ, ZZZ)"
        )

        self.assertEqual(steps_to_end(example), 6)

    def test_part_2(self):
        example = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
        
        self.assertEqual(steps_to_all_z(example), 6)


if __name__ == "__main__":
    with open("advent/2023/input_2023_8.txt", "r") as f:
        text = f.read()
        result = steps_to_end(text)

        print(f"2023 Day 8: Part 1: {result=}")

    with open("advent/2023/input_2023_8.txt", "r") as f:
        text = f.read()
        result = steps_to_all_z(text)

        print(f"2023 Day 8: Part 2: {result=}")
