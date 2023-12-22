import collections as C
import re
from unittest import TestCase

example = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

# Amazed by this solution: https://www.reddit.com/r/adventofcode/comments/18o7014/comment/kegg6n0/?utm_source=reddit&utm_medium=web2x&context=3
# I wanted to keep it myself.

def drop(stack, skip=None):
    peaks = C.defaultdict(int)
    falls = 0

    for i, (u, v, w, x, y, z) in enumerate(stack):
        if i == skip:
            continue

        area = [(a, b) for a in range(u, x + 1) for b in range(v, y + 1)]
        peak = max(peaks[a] for a in area) + 1
        for a in area:
            peaks[a] = peak + z - w

        stack[i] = (u, v, peak, x, y, peak + z - w)
        falls += peak < w

    return not falls, falls


def get_stack(input_str: str):
    input = input_str.split("\n")
    return sorted(
        [[*map(int, re.findall(r"\d+", l))] for l in input], key=lambda b: b[2]
    )


def wow(input):
    stack = get_stack(input)
    drop(stack)
    return [*map(sum, zip(*[drop(stack.copy(), skip=i) for i in range(len(stack))]))]


class AdventTest(TestCase):
    def test_example(self):
        self.assertEqual(wow(example), [5,7])


if __name__ == "__main__":
    with open("advent/2023/input_2023_22.txt") as input:
        print(wow(input.read()))