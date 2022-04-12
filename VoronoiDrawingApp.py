import pygame as pg

from VoronoiNetworkMaker import VoronoiNetworkMaker


class VoronoiDrawingApp:

    RADIUS = 8

    def __init__(self, x, y, pts):
        pg.init()
        pg.display.set_mode((x, y))
        self.x = x
        self.y = y
        self.n = pts
        self.surface = pg.display.get_surface()
        self.network = net = VoronoiNetworkMaker(pts, x, y)

    def _draw_edge_lines(self, edges, colour):
        for e in edges:
            pg.draw.line(surface=self.surface,
                         color=colour,
                         width=self.RADIUS,
                         start_pos=e[0],
                         end_pos=e[1])

    def draw(self):
        inlet, network, outlet = self.network.edges_partitioned
        self._draw_edge_lines(inlet, (0, 255, 0))
        self._draw_edge_lines(network, (255, 0, 0))
        self._draw_edge_lines(outlet, (0, 255, 255))
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
    app = VoronoiDrawingApp(800, 800, 50)
    app.run()
