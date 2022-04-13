import random
from math import sqrt

from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

from LinAlg import LineSegment, Vec2D


def edge_length(e):
    u, v = e
    x = abs(u[0] - v[0])
    y = abs(u[1] - v[1])
    return sqrt(x**2 + y**2)


class VoronoiNetworkMaker:

    def __init__(self, n, x, y):
        self.x = x
        self.y = y
        pts = [self.random_point() for _ in range(n)] + [(-x, -y), (2 * x, -y), (-x, 2 * y), (2 * x, 2 * y)]
        self.vor = Voronoi(pts)
        self.adj = self._make_adjacency_list()

    def _make_adjacency_list(self):
        vertices = list(self.vertices)
        adj = {v: [] for v in vertices}
        for pair in self.vor.ridge_vertices:
            i, j = pair[0], pair[1]
            if i == -1 or j == -1:
                continue
            u, v = vertices[i], vertices[j]
            adj[u].append(v)
            adj[v].append(u)
        return adj

    def random_point(self):
        x = random.randrange(0, self.x)
        y = random.randrange(0, self.y)
        return x, y

    def contains_vertex(self, vertex):
        i, j = vertex[0], vertex[1]
        return not (i < 0 or i > self.x or j < 0 or j > self.y)

    @property
    def vertices(self):
        for v in self.vor.vertices:
            yield v[0], v[1]

    @property
    def network_vertices(self):
        for v in self.vertices:
            if self.contains_vertex(v):
                yield v

    @property
    def supply(self):
        """For each vertex, a positive number is the number of units of flow that this vertex supplies, and a
        negative number is the number of units of flow that this vertex receives."""
        adj = self.adj
        supply = {v: 0 for v in self.network_vertices}
        total = 0
        for v in self.network_vertices:
            # We need to count the adjacent vertices that are LEFT of the screen.
            for i, _ in adj[v]:
                if i < 0:
                    supply[v] += 1
                    total += 1
        # Now, rescale so that a single unit of flow is supplied in total.
        for v in supply.keys():
            supply[v] = supply[v] / total
        return supply

    @property
    def demand(self):
        adj = self.adj
        demand = {v: 0 for v in self.network_vertices}
        total = 0
        for v in self.network_vertices:
            for i, _ in adj[v]:
                if i > self.x:
                    demand[v] -= 1
                    total += 1
        if total > 0:
            for v in demand.keys():
                demand[v] = demand[v] / total
        return demand

    @property
    def supply_demand(self):
        s = self.supply
        d = self.demand
        return {v: s[v] + d[v] for v in self.network_vertices}

    @property
    def network_edges(self):
        for e in self.edges:
            u, v = e    # Get the edge vertices
            if self.contains_vertex(u) and self.contains_vertex(v):
                yield e

    def compute_pressures_flows(self):
        pass

    @property
    def edges(self):
        def round_pair(p):
            return round(p[0]), round(p[1])
        vertices = self.vor.vertices
        for pair in self.vor.ridge_vertices:
            i, j = pair[0], pair[1]
            if i == -1 or j == -1:
                continue
            yield tuple(vertices[i]), tuple(vertices[j])

    @property
    def edges_partitioned(self):
        network_edges = []
        inlet_edges = []
        outlet_edges = []
        for e in self.edges:
            u, v = e
            if u[0] < 0 or v[0] < 0:
                inlet_edges.append(e)
            elif u[0] > self.x or v[0] > self.x:
                outlet_edges.append(e)
            else:
                network_edges.append(e)
        return inlet_edges, network_edges, outlet_edges

    def distance_from_vessel(self, point):
        """Approximate the smallest distance from the given point to another vessel. Only consider network edges.
        :returns the distance, and the vessel involved.
        """
        vessels = list(self.network_edges)
        p = Vec2D.from_tuple(point)

        def make_tuple(v):
            # Contains the distance to the vessel, and the endpoints of the vessel.
            a = Vec2D.from_tuple(v[0])
            b = Vec2D.from_tuple(v[1])
            s = LineSegment(a, b)
            d = s.distance_to(p)
            return d, v
        # The distance to the nearest vessel.
        return min(make_tuple(v) for v in vessels)

    def greatest_distance_from_vessel(self, interval):
        points = []
        for i in range(0, self.x, interval):
            for j in range(0, self.x, interval):
                points.append((i, j))
        vessel_distances = [(self.distance_from_vessel(p), p) for p in points]
        (d, e), v = max(vessel_distances)
        return d, v, e

    def draw(self, lim=None):
        #print(self.vor.vertices)
        #print(self.vor.ridge_vertices)

        #vertices = self.vor.vertices
        #all_ridges = self.vor.ridge_vertices
        #def out_of_bounds(i):
        #    return (vertices[i][0] < 0 or vertices[i][0] > self.x) and (vertices[i][1] < 0 or vertices[i][1] > self.y)
        #no_double_outside = [[i, j] for [i, j] in all_ridges if not out_of_bounds(i) or not out_of_bounds(j)]
        #print(no_double_outside)
        #print(list(self.edges))


        fig = voronoi_plot_2d(self.vor, show_points=True, show_vertices=True, s=4)

        plt.xlim((-self.x, 2 * self.x))
        plt.ylim((-self.y, 2 * self.y))
        plt.show()


if __name__ == "__main__":
    v = VoronoiNetworkMaker(200, 500, 500)
    print(list(v.vertices))
    print(v.adj)
    print(v.supply_demand)
    for i in range(0, v.x, 25):
        for j in range(0, v.y, 25):
            print((i, j), v.distance_from_vessel((i, j)))
    v.draw()
