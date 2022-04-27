from __future__ import annotations

from queue import PriorityQueue, Queue, LifoQueue
from random import random

import numpy as np

from utils import concat


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
    def indices(self):
        return self.i, self.j

    @property
    def is_discovered(self):
        return self.discovered != -1

    @property
    def is_reached(self):
        return self.reached != -1

    def edge_to(self, other):
        edges = [e for e in self.edges if e.touches(other)]
        assert len(edges) == 1
        return edges[0]


class Edge:

    def __init__(self, a, b):
        self.a = a
        self.b = b
        a.edges.append(self)
        b.edges.append(self)

    def touches(self, c):
        return self.a is c or self.b is c

    def other(self, c):
        assert c is self.a or c is self.b
        return self.b if c is self.a is c else self.a


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
    def cells(self) -> List[List[Cell]]:
        """A 2D list of the cells in the graph. """
        return self._cells

    @property
    def nodes(self) -> List[(int, int)]:
        return concat([c.indices for c in self._cells])

    @property
    def edges(self) -> List[Edge]:
        """A 2D list of the edges in the graph. """
        return self._edges

    @property
    def adjacency_list(self):
        """Return an adjacency list in the form of a dictionary. """
        return {c: [e.a if e.a is not c else e.b for e in c.edges] for c in concat(self._cells)}

    def compute_manhattan_distances(self, predicate):
        """Compute and :return the Manhattan distance of each cell from the cells satisfying a given predicate. """
        q = Queue()
        distances = [[None for _ in range(self.y)] for _ in range(self.x)]
        for c in concat(self.cells):
            if predicate(c):
                q.put((c, 0))
        while not q.empty():
            c, n = q.get()
            if distances[c.i][c.j] is None:
                distances[c.i][c.j] = n
                for d in self._get_cell_neighbours(c):
                    q.put((d, n + 1))
        return distances

    def compute_pressures(self, leaky=False):
        """Compute and :return the pressure at each cell in the network. """
        return self._compute_pressures_no_leaky() if leaky == False else self._compute_pressures_leaky()

    def _compute_pressures_no_leaky(self):
        # Do a linear algebra calculation to compute the flows in the system.
        # By convention, "towards the bottom left corner" is the positive direction.
        R = 1   # The resistance of a vessel.
        cells = tuple(c for c in concat(self.cells) if c.is_reached)
        edges = tuple(self.edges)
        start = self.top_left
        end = self.bottom_right
        cell_indices = {c: i for i, c in enumerate(cells)}  # To quickly look up the index of a cell.
        edge_indices = {e: i for i, e in enumerate(edges)}  # To quickly look up the index of an edge.
        matrix = []
        result = []
        q_num = len(edges)  # There is a variable for every line segment.
        p_num = len(cells)  # There is a variable for every cell.

        # some helper functions
        def q(e: Edge): return edge_indices[e]

        def p(c: Cell): return q_num + cell_indices[c]

        def find_edge(a, b):
            # Find the edge that connects a and b
            for e in a.edges:
                if (e.a is a and e.b is b) or (e.b is a and e.a is b):
                    return e
            assert False

        def minmax(e):
            a = e.a
            b = e.b
            return (a, b) if cell_indices[a] < cell_indices[b] else (b, a)

        for i, c in enumerate(cells):
            # At each cell, we need the input and output flows to add to 0.
            if c is start:  # We don't count the start cell. This ensures that our matrix is full rank.
                continue
            result.append((0 if c is not end else 1,))  # Only the endpoint is allowed to have flow exit the system.

            this_row = [0 for _ in range(q_num + p_num)]
            for e in c.edges:
                assert e in edges   # TODO: Remove this since it's expensive!
                a, b = minmax(e)
                assert cell_indices[a] < cell_indices[b]  # Check
                assert (a is c or b is c) and (a is not c or b is not c)
                this_row[q(e)] = 1 if b is c else -1
            matrix.append(this_row)

        for i, e in enumerate(edges):
            result.append((0,))
            this_row = [0 for _ in range(q_num + p_num)]
            # At each edge, we want the pressure drop to equal the resistance (1) times the flow.
            a, b = minmax(e)
            assert cell_indices[a] < cell_indices[b]  # Check
            this_row[p(a)] = 1
            this_row[p(b)] = -1
            this_row[q(e)] = -R
            matrix.append(this_row)

        # A final row to fix the output pressure at 0.
        this_row = [0 for _ in range(q_num + p_num)]
        this_row[p(end)] = 1
        matrix.append(this_row)
        result.append((0,))

        mat = np.array(matrix)
        res = np.array(result)

        #print("Reached")
        #print(mat)
        #print(res)
        pressures_flows = np.linalg.solve(mat, res)
        #print(pressures_flows)

        # we have the results. so find the associated cell and edge.

        flow_results = [(e, pressures_flows[q(e), 0]) for e in edges]
        pressure_results = [(c, pressures_flows[p(c), 0]) for c in cells]

        #print(pressure_results)
        #print(flow_results)

        return flow_results, pressure_results

    def _compute_pressures_leaky(self):
        pass  # TODO: _compute_pressures_leaky

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

    @property
    def top_left(self):
        _, res = self.find_top_left()
        assert res.is_reached
        return res

    def find_top_left(self):
        # TODO: Currently only works on square networks!
        failures = []
        for i in range(self.x):
            for j in range(i + 1):
                c = self._cells[i - j][j]
                if c.is_reached:
                    return failures, c
                failures.append(c)

    @property
    def bottom_right(self):
        _, res = self.find_bottom_right()
        assert res.is_reached
        return res

    def find_bottom_right(self):
        # TODO: Currently only works on square networks!
        failures = []
        for i in range(self.x):
            for j in range(i + 1):
                c = self._cells[self.x - i + j - 1][self.y - j - 1]
                if c.is_reached:
                    return failures, c
                failures.append(c)

    def bfs(self, start):
        q = Queue()
        adj = self.adjacency_list
        distances = {c: None for c in concat(self._cells)}
        backrefs = {c: None for c in concat(self._cells)}
        distances[start] = 0
        q.put(start)
        while not q.empty():
            u = q.get()
            for v in adj[u]:
                if distances[v] is None:
                    distances[v] = distances[u] + 1
                    backrefs[v] = u
                    q.put(v)
        return backrefs

    def remove_dead_ends(self):
        """Remove the dead ends from the network.
        :returns a list of the edges after the dead ends have been removed.
        """
        source = self.top_left
        sink = self.bottom_right
        adj = self.adjacency_list
        deleted = {e: False for e in self._edges}
        nodes_deleted = {c: False for c in concat(self._cells)}

        def can_find(start, no_visit):
            # Can we find the source or the sink without ever visiting the node no_visit?
            s = LifoQueue()
            discovered = {c: False for c in concat(self._cells)}
            discovered[start] = True
            s.put(start)
            while not s.empty():
                u = s.get()
                if u is source or u is sink:
                    return True
                for v in adj[u]:
                    if v is not no_visit and not discovered[v]:
                        discovered[v] = True
                        s.put(v)
            return False

        def delete_scc_conditional(start, no_visit):
            if not can_find(start, no_visit):
                s = LifoQueue()
                nodes_deleted[start] = True
                s.put(start)
                while not s.empty():
                    u = s.get()
                    for v in adj[u]:
                        if v is not no_visit and not nodes_deleted[v]:
                            nodes_deleted[v] = True
                            s.put(v)

        for e in self._edges:
            if not deleted[e]:
                delete_scc_conditional(e.a, e.b)
                delete_scc_conditional(e.b, e.a)
        # Return the nodes and the edges.
        return [v for v in concat(self._cells) if v.is_reached and not nodes_deleted[v]], \
               [e for e in self._edges if not nodes_deleted[e.a] and not nodes_deleted[e.b]]

    @property
    def shortest_path_edges(self):
        start = self.top_left
        backrefs = self.bfs(start)
        succ = self.bottom_right
        edges = []
        while succ is not start:
            pred = backrefs[succ]
            assert pred is not None
            edges.append(pred.edge_to(succ))
            succ = pred
        return edges

    #def remove_dead_ends(self, cells):
    #    # TODO: Make a real cell not a dummy cell
    #    not_dead_end = [[c for c in row] for row in cells]  # Copy cells
    #    for i, row in enumerate(cells):
    #        for j, c in enumerate(row):
    #            if not c.is_reached:
    #                not_dead_end[c.i][c.j] = None
    #    cells_to_expand = set()
    #    for row in cells:
    #        for c in row:
    #            cells_to_expand.add(c)
    #    # cells_to_expand now contains all cells
    #    while len(cells_to_expand) > 0:
    #        c = cells_to_expand.pop()
    #        ns = [n for n in self._get_cell_neighbours(c) if n.is_reached]
    #        if len(ns) == 1:  # Then it is a dead end
    #            print("Reached!")
    #            not_dead_end[c.i][c.j] = None  # Don't include the cell at this position
    #            cells_to_expand.add(ns[0])
    #    return not_dead_end

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
    m = InvasionPercolationNetwork(50, 50, 0.3)
    cells, _ = m.make_network()
    a = [[True if c.is_reached else False for c in row] for row in cells]
    print(np.array(a))


if __name__ == "__main__":
    main()
