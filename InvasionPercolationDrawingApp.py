import pygame as pg

from InvasionPercolationNetworkMaker import InvasionPercolationNetworkMaker


class InvasionPercolationDrawingApp:

    INTERVAL = 5

    def __init__(self, x, y, occ):
        self.x = x
        self.y = y
        self.occ = occ
        pg.display.set_mode((x * self.INTERVAL, y * self.INTERVAL))
        self.surface = pg.display.get_surface()
        self.maker = m = InvasionPercolationNetworkMaker(x, y, occ)
        _, self.edges = m.make_network()

    def get_coords(self, a):
        x_coord = self.INTERVAL // 2 + a.i * self.INTERVAL
        y_coord = self.INTERVAL // 2 + a.j * self.INTERVAL
        return x_coord, y_coord

    def draw(self):
        for e in self.edges:
            pg.draw.line(surface=self.surface,
                         color=(255, 0, 0),
                         width=self.INTERVAL // 5,
                         start_pos=self.get_coords(e.a),
                         end_pos=self.get_coords(e.b))
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
    app = InvasionPercolationDrawingApp(200, 200, 0.03)
    app.run()