import pygame as pg

from VoronoiNetworkMaker import VoronoiNetworkMaker


class VoronoiDrawingApp:

    RADIUS = 8      # Really the width of a vessel
    INTERVAL = 25   # The interval to use when checking oxygenation of points

    def __init__(self, x, y, pts):
        pg.init()
        pg.display.set_mode((x, y))
        self.x = x
        self.y = y
        self.n = pts
        self.surface = pg.display.get_surface()
        self.network = net = VoronoiNetworkMaker(pts, x, y)
        self.distances = []
        for i in range(0, x, self.INTERVAL):
            for j in range(0, y, self.INTERVAL):
                self.distances.append(((i, j), net.distance_from_vessel((i, j))))
        print(net.greatest_distance_from_vessel(self.INTERVAL))
        self.index = 0

    def _draw_edge_lines(self, edges, colour, width):
        for e in edges:
            pg.draw.line(surface=self.surface,
                         color=colour,
                         width=width,
                         start_pos=e[0],
                         end_pos=e[1])

    def _draw_vertex_circles(self, vertices, colour, radius):
        for v in vertices:
            pg.draw.circle(surface=self.surface,
                           color=colour,
                           radius=radius,
                           center=v)

    def draw(self, index):
        self.surface.fill((0, 0, 0))
        inlet, network, outlet = self.network.edges_partitioned
        self._draw_edge_lines(inlet, (0, 255, 0), self.RADIUS)
        self._draw_edge_lines(network, (255, 0, 0), self.RADIUS)
        self._draw_edge_lines(outlet, (0, 255, 255), self.RADIUS)
        v, (d, (u1, u2)) = self.distances[index]

        self._draw_vertex_circles((v,), (0, 0, 255), 10)
        self._draw_edge_lines(((u1, u2),), (0, 0, 255), 5)
        print(d)
        pg.display.flip()

    def run(self):
        i = 200
        n = len(self.distances)
        self.draw(i)
        x_index_change = self.y // self.INTERVAL
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP and i % x_index_change >= 1:
                        self.draw(i := i - 1)
                    if event.key == pg.K_DOWN and i % x_index_change < x_index_change - 1:
                        self.draw(i := i + 1)
                    if event.key == pg.K_LEFT and i >= x_index_change:
                        self.draw(i := i - x_index_change)
                    if event.key == pg.K_RIGHT and i < n - x_index_change:
                        self.draw(i := i + x_index_change)


if __name__ == "__main__":
    app = VoronoiDrawingApp(800, 800, 100)
    app.run()
