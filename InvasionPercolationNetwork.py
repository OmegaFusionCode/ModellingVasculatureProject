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


class InvasionPercolationNetwork:

    def __init__(self, x: int, y: int, occupancy: float):
        assert 0.0 <= occupancy <= 1.0
        self.x = x
        self.y = y
        self.n = round(x * y * occupancy)
        self._cells = None
        self._edges = None
        self._q = None
        self._make_network()

    @property
    def cells(self):
        return self._cells

    @property
    def edges(self):
        return self._edges

    def _generate_random_capacities(self):
        return [[random() for _ in range(self.y)] for _ in range(self.x)]

    def _get_cell_neighbours(self, c):
        i, j = c.i, c.j
        neighbours = []
        if i > 0:
            neighbours.append(self.cells[i - 1][j])
        if i < self.x - 1:
            neighbours.append(self.cells[i + 1][j])
        if j > 0:
            neighbours.append(self.cells[i][j - 1])
        if j < self.x - 1:
            neighbours.append(self.cells[i][j + 1])
        return neighbours

    def _discover_cells(self, cs, t):
        for c in cs:
            if not c.is_discovered:
                c.discovered = t
                self._q.put(c)

    def _add_edges(self, cells, a):
        assert a.is_reached
        for b in cells:
            if b.is_reached:
                e = Edge(a, b)
                self._edges.append(e)

    def _initially_discover(self, i, j):
        c = self._cells[i][j]
        c.reached = 0
        c.discovered = 0
        # Neighbours must be added to the queue properly.
        ns = self._get_cell_neighbours(c)
        self._discover_cells(ns, 0)

    def _make_network(self):
        self._q = PriorityQueue()
        caps = self._generate_random_capacities()
        # Put in the queue each capacity along with its coordinates.
        self._cells = [[Cell(v, i, j) for j, v in enumerate(row)] for i, row in enumerate(caps)]
        self._edges = []
        # Some cells are initially discovered.
        self._initially_discover(self.x // 2, self.y // 2)
        # self._initially_discover(cells, self.x-1, self.y-1, q)

        for t in range(1, self.n + 1):
            cell = self._q.get()
            assert cell.is_discovered
            assert not cell.is_reached
            cell.reached = t
            assert cell.is_reached
            neighbours = self._get_cell_neighbours(cell)
            self._discover_cells(neighbours, t)
            self._add_edges(neighbours, cell)

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

    def remove_dead_ends(self, cells):
        # TODO: Make a real cell not a dummy cell
        not_dead_end = [[c for c in row] for row in cells]     # Copy cells
        for i, row in enumerate(cells):
            for j, c in enumerate(row):
                if not c.is_reached:
                    not_dead_end[c.i][c.j] = None
        cells_to_expand = set()
        for row in cells:
            for c in row:
                cells_to_expand.add(c)
        # cells_to_expand now contains all cells
        while len(cells_to_expand) > 0:
            c = cells_to_expand.pop()
            ns = [n for n in self._get_cell_neighbours(c) if n.is_reached]
            if len(ns) == 1:   # Then it is a dead end
                print("Reached!")
                not_dead_end[c.i][c.j] = None  # Don't include the cell at this position
                cells_to_expand.add(ns[0])
        return not_dead_end

    def find_most_distant_point(self, cells):
        pq = PriorityQueue()
        added = [[False for _ in row] for row in cells]

        def add_cell_neighbours(distance, cell):
            for next_cell in self._get_cell_neighbours(cell):
                if not added[next_cell.i][next_cell.j]:
                    pq.put((distance + 1, next_cell))
                    added[next_cell.i][next_cell.j] = True

        furthest = None
        for row in cells:
            for c in row:
                if c.is_reached:
                    added[c.i][c.j] = True
                    add_cell_neighbours(0, c)
        while not pq.empty():
            d, c = pq.get()
            furthest = d, c
            add_cell_neighbours(d, c)
        return furthest


def main():
    m = InvasionPercolationNetwork(10, 10, 0.3)
    cells, _ = m.make_network()
    a = [[True if c.is_reached else False for c in row] for row in cells]
    print(np.array(a))


if __name__ == "__main__":
    main()
