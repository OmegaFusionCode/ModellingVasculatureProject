import pygame as pg

from InvasionPercolationNetworkMaker import InvasionPercolationNetworkMaker


class InvasionPercolationDrawingApp:
    INTERVAL = 100

    def __init__(self, x, y, occ):
        self.x = x
        self.y = y
        self.occ = occ
        pg.display.set_mode((x * self.INTERVAL, y * self.INTERVAL))
        self.surface = pg.display.get_surface()
        self.maker = m = InvasionPercolationNetworkMaker(x, y, occ)
        cells, self.edges = m.make_network()
        self.failures_top_left, self.top_left = m.find_top_left(cells)
        self.failures_bottom_right, self.bottom_right = m.find_bottom_right(cells)
        a = m.bfs(self.top_left)
        print("Reached")
        self.shortest_path_edges = []
        curr = self.bottom_right
        while curr is not self.top_left:
            curr, e = a[curr.i][curr.j]
            self.shortest_path_edges.append(e)

    def get_coords(self, a):
        x_coord = self.INTERVAL // 2 + a.i * self.INTERVAL
        y_coord = self.INTERVAL // 2 + a.j * self.INTERVAL
        return x_coord, y_coord

    def draw(self):
        for c in self.failures_top_left + self.failures_bottom_right:
            pg.draw.circle(surface=self.surface,
                           color=(255, 255, 0),
                           radius=self.INTERVAL // 2,
                           center=self.get_coords(c))
        for c in [self.top_left, self.bottom_right]:
            pg.draw.circle(surface=self.surface,
                           color=(255, 0, 255),
                           radius=self.INTERVAL // 2,
                           center=self.get_coords(c))
        for e in self.edges:
            pg.draw.line(surface=self.surface,
                         color=(255, 0, 0),
                         width=self.INTERVAL // 5,
                         start_pos=self.get_coords(e.a),
                         end_pos=self.get_coords(e.b))
        for e in self.shortest_path_edges:
            pg.draw.line(surface=self.surface,
                         color=(0, 255, 0),
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
    app = InvasionPercolationDrawingApp(10, 10, 0.55)
    app.run()
