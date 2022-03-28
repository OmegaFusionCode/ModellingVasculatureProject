import pygame as pg
import numpy as np

from InvasionPercolationNetwork import InvasionPercolationNetwork


class InvasionPercolationDrawingApp:
    INTERVAL = 10

    def __init__(self, x, y, occ):
        self.x = x
        self.y = y
        self.occ = occ
        pg.display.set_mode((x * self.INTERVAL, y * self.INTERVAL))
        self.surface = pg.display.get_surface()
        self.network = net = InvasionPercolationNetwork(x, y, occ)
        self.failures_top_left, self.top_left = net.find_top_left()
        self.failures_bottom_right, self.bottom_right = net.find_bottom_right()
        #a = net.bfs(self.top_left)
        #self.shortest_path_edges = []
        #curr = self.bottom_right
        #while curr is not self.top_left:
        #    curr, e = a[curr.i][curr.j]
        #    self.shortest_path_edges.append(e)
        self.remote_distance, self.remote_cell = net.find_most_distant_point(net.cells)
        #print(self.remote_distance)
        #print(self.remote_cell.i, self.remote_cell.j)
        #for c, es in net.adjacency_list.items():
        #    print(f"({c.i},{c.j}) - {es}")
        distances = net.compute_manhattan_distances(lambda c: c.is_reached)
        dead_end_nodes, self.dead_ends = net.remove_dead_ends()
        distances_no_dead_ends = net.compute_manhattan_distances(lambda c: c in dead_end_nodes)
        #shortest_path_nodes = net.shortest_path_edges()
        #f = lambda v, e: v is e.a or v is e.b  # TODO: This
        print(np.matrix(distances).transpose())
        print(np.matrix(distances_no_dead_ends).transpose())
        print(len(net.edges))
        print(net.compute_pressures(leaky=False))


    def get_coords(self, a):
        x_coord = self.INTERVAL // 2 + a.i * self.INTERVAL
        y_coord = self.INTERVAL // 2 + a.j * self.INTERVAL
        return x_coord, y_coord

    def _draw_vertex_circles(self, cells, colour):
        for c in cells:
            pg.draw.circle(surface=self.surface,
                           color=colour,
                           radius=self.INTERVAL // 2,
                           center=self.get_coords(c))

    def _draw_edge_lines(self, edges, colour):
        for e in edges:
            pg.draw.line(surface=self.surface,
                         color=colour,
                         width=self.INTERVAL // 5,
                         start_pos=self.get_coords(e.a),
                         end_pos=self.get_coords(e.b))

    def draw(self):
        #for c in self.failures_top_left + self.failures_bottom_right:
        #    pg.draw.circle(surface=self.surface,
        #                   color=(255, 255, 0),
        #                   radius=self.INTERVAL // 2,
        #                   center=self.get_coords(c))
        #for c in [self.top_left, self.bottom_right]:
        #    pg.draw.circle(surface=self.surface,
        #                   color=(255, 0, 255),
        #                   radius=self.INTERVAL // 2,
        #                   center=self.get_coords(c))
        # Geometrically Most Remote Point
        #for i, row in enumerate(self.network.remove_dead_ends(self.network.cells)):
        #    for j, c in enumerate(row):
        #        if c is not None:
        #            pg.draw.circle(surface=self.surface,
        #                           color=(255, 255, 0),
        #                           radius=self.INTERVAL // 2,
        #                           center=self.get_coords(c))
        self._draw_vertex_circles((self.remote_cell,), (255, 0, 255))
        self._draw_edge_lines(self.network.edges, (255, 0, 0))
        self._draw_edge_lines(self.dead_ends, (0, 255, 0))
        self._draw_edge_lines(self.network.shortest_path_edges, (255, 0, 255))
        pg.display.flip()

    def run(self):
        self.draw()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    running = False


if __name__ == "__main__":
    app = InvasionPercolationDrawingApp(5, 5, 0.55)
    app.run()
