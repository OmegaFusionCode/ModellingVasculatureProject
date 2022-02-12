from queue import PriorityQueue
from random import random

import numpy as np


class Cell:

    def __init__(self, capacity, i, j):
        self.c = capacity
        self.i = i
        self.j = j
        self.discovered = -1
        self.reached = -1

    def __lt__(self, other):
        return self.c < other.c

    @property
    def is_discovered(self):
        return self.discovered != -1

    @property
    def is_reached(self):
        return self.reached != -1


class InvasionPercolationNetworkMaker:

    def __init__(self, x: int, y: int, occupancy: float):
        assert 0.0 <= occupancy <= 1.0
        self.x = x
        self.y = y
        self.n = round(x * y * occupancy)

    def _generate_random_capacities(self):
        return [[random() for _ in range(self.y)] for _ in range(self.x)]

    def _get_cell_neighbours(self, cells, c):
        i, j = c.i, c.j
        neighbours = []
        if i > 0:
            neighbours.append(cells[i-1][j])
        if i < self.x-1:
            neighbours.append(cells[i+1][j])
        if j > 0:
            neighbours.append(cells[i][j-1])
        if j < self.x-1:
            neighbours.append(cells[i][j+1])
        return neighbours

    @staticmethod
    def _discover_cells(cs, t, q):
        for c in cs:
            if not c.is_discovered:
                c.discovered = t
                q.put(c)

    def make_network(self):
        q = PriorityQueue()
        caps = self._generate_random_capacities()
        # Put in the queue each capacity along with its coordinates.
        cells = [[Cell(v, i, j) for j, v in enumerate(row)] for i, row in enumerate(caps)]
        # Some cells are initially discovered.
        start = cells[0][0]
        start.reached = 0
        start.discovered = 0
        # Neighbours must be added to the queue properly.
        ns = self._get_cell_neighbours(cells, start)
        self._discover_cells(ns, 0, q)

        for t in range(1, self.n+1):
            cell = q.get()
            assert cell.is_discovered
            assert not cell.is_reached
            cell.reached = t
            assert cell.is_reached
            neighbours = self._get_cell_neighbours(cells, cell)
            self._discover_cells(neighbours, t, q)

        return [[True if c.is_reached else False for c in row] for row in cells]



if __name__ == "__main__":
    m = InvasionPercolationNetworkMaker(10, 10, 0.5)
    network = m.make_network()
    print(np.array(network))
