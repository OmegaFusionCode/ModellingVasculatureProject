from queue import PriorityQueue, Queue
from random import random

import numpy as np


class Cell:

    def __init__(self, capacity, i, j):
        self.c = capacity
        self.i = i
        self.j = j
        self.discovered = -1
        self.reached = -1
        self.edges = []

    def __lt__(self, other):
        return self.c < other.c

    @property
    def is_discovered(self):
        return self.discovered != -1

    @property
    def is_reached(self):
        return self.reached != -1


class Edge:

    def __init__(self, a, b):
        self.a = a
        self.b = b
        a.edges.append(self)
        b.edges.append(self)


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
            neighbours.append(cells[i - 1][j])
        if i < self.x - 1:
            neighbours.append(cells[i + 1][j])
        if j > 0:
            neighbours.append(cells[i][j - 1])
        if j < self.x - 1:
            neighbours.append(cells[i][j + 1])
        return neighbours

    @staticmethod
    def _discover_cells(cs, t, q):
        for c in cs:
            if not c.is_discovered:
                c.discovered = t
                q.put(c)

    def _add_edges(self, cells, a, edges):
        assert a.is_reached
        for b in cells:
            if b.is_reached:
                e = Edge(a, b)
                edges.append(e)

    def _initially_discover(self, cells, i, j, q):
        c = cells[i][j]
        c.reached = 0
        c.discovered = 0
        # Neighbours must be added to the queue properly.
        ns = self._get_cell_neighbours(cells, c)
        self._discover_cells(ns, 0, q)

    def make_network(self):
        q = PriorityQueue()
        caps = self._generate_random_capacities()
        # Put in the queue each capacity along with its coordinates.
        cells = [[Cell(v, i, j) for j, v in enumerate(row)] for i, row in enumerate(caps)]
        edges = []
        # Some cells are initially discovered.
        self._initially_discover(cells, self.x // 2, self.y // 2, q)
        # self._initially_discover(cells, self.x-1, self.y-1, q)

        for t in range(1, self.n + 1):
            cell = q.get()
            assert cell.is_discovered
            assert not cell.is_reached
            cell.reached = t
            assert cell.is_reached
            neighbours = self._get_cell_neighbours(cells, cell)
            self._discover_cells(neighbours, t, q)
            self._add_edges(neighbours, cell, edges)
        return cells, edges

    def find_top_left(self, cells):
        # TODO: Currently only works on square networks!
        failures = []
        for i in range(self.x):
            for j in range(i + 1):
                c = cells[i - j][j]
                if c.is_reached:
                    return failures, c
                failures.append(c)

    def find_bottom_right(self, cells):
        # TODO: Currently only works on square networks!
        failures = []
        for i in range(self.x):
            for j in range(i + 1):
                c = cells[self.x - i + j - 1][self.y - j - 1]
                if c.is_reached:
                    return failures, c
                failures.append(c)

    def bfs(self, start):
        q = Queue()
        distances = [[None for _ in range(self.y)] for _ in range(self.x)]
        backrefs = [[None for _ in range(self.y)] for _ in range(self.x)]
        distances[start.i][start.j] = 0
        q.put(start)
        while not q.empty():
            u = q.get()
            for e in u.edges:
                v = e.a if e.a is not u else e.b  # Get the other end of this edge.
                if distances[v.i][v.j] is None:
                    distances[v.i][v.j] = distances[u.i][u.j] + 1
                    backrefs[v.i][v.j] = u, e
                    q.put(v)
        return backrefs


def main():
    m = InvasionPercolationNetworkMaker(10, 10, 0.3)
    cells, _ = m.make_network()
    a = [[True if c.is_reached else False for c in row] for row in cells]
    print(np.array(a))


if __name__ == "__main__":
    main()
