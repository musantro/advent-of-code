'''
This was a pretty good explanation (spanish)
https://www.youtube.com/watch?v=fgdCNuGPJnw
'''

from collections import defaultdict
from heapq import heappop, heappush
from math import inf
from unittest import TestCase


def dijkstra(grid, lo, hi):
    n, m = len(grid), len(grid[0])
    dists = defaultdict(lambda: inf)
    heap = [(0, (0, 0, (0, 1))), (0, (0, 0, (1, 0)))]
    while heap:
        cost, (i, j, d) = heappop(heap)
        if (i, j) == (n - 1, m - 1):
            return cost
        if cost > dists[i, j, d]:
            continue
        di, dj = d
        for ndi, ndj in ((-dj, di), (dj, -di)):
            ncost = cost
            for dist in range(1, hi + 1):
                ni, nj = i + ndi * dist, j + ndj * dist
                if 0 <= ni < n and 0 <= nj < m:
                    ncost += int(grid[ni][nj])
                    if dist < lo:
                        continue
                    k = (ni, nj, (ndi, ndj))
                    if ncost < dists[k]:
                        dists[k] = ncost
                        heappush(heap, (ncost, k))
    return -1


example = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""


class AdventTest(TestCase):
    def test_part_1(self):
        self.assertEqual(dijkstra(example.split("\n"), 1, 3), 102)
    def test_part_2(self):
        self.assertEqual(dijkstra(example.split("\n"), 4, 10), 94)


if __name__ == "__main__":
    with open("advent/2023/input_2023_17.txt", "r") as file:
        data = file.read().strip()

    GRID = data.split("\n")

    print(f"2023 Day 17: Part 1: {dijkstra(GRID, 1, 3)}")
    print(f"2023 Day 17: Part 2g: {dijkstra(GRID, 4, 10)}")
