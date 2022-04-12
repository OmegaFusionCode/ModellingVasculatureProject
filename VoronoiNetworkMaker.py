import random

from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt


class VoronoiNetworkMaker:

    def __init__(self, n, x, y):
        self.x = x
        self.y = y
        pts = [self.random_point() for _ in range(n)] + [(-x, -y), (2 * x, -y), (-x, 2 * y), (2 * x, 2 * y)]
        self.vor = Voronoi(pts)

    def random_point(self):
        x = random.randrange(0, self.x)
        y = random.randrange(0, self.y)
        return x, y

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
        self.draw()

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
    v = VoronoiNetworkMaker(200, 100, 100)
    v.draw()
