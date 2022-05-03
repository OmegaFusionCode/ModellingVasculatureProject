import csv
import logging

import pygame as pg

INTERVAL = 15
X = Y = 800


class CCOHeatMapDrawer:

    def __init__(self):
        pg.init()
        pg.display.set_mode((X, Y))
        self.surface = pg.display.get_surface()
        points, terminal = self.read_data("terminal")
        points_vessel, vessel = list(self.read_data("vessel"))
        assert points_vessel == points
        self.data = (terminal, vessel)
        self.points = points

    @staticmethod
    def read_data(filename):
        points = []
        data = []
        with open(f"results/cco/{filename}.txt") as tsv:
            first_line = True
            for line in csv.reader(tsv, delimiter="\t"):
                if first_line:
                    first_line = False
                    continue
                def f(n):
                    return round(float(n))
                points.append(tuple(map(f, line[0].strip("(").strip(")").split(","))))
                data.append(float(line[1]))
        return points, data

    def _draw_circle(self, point, colour):
        print(f"Drawing {point}")
        pg.draw.circle(surface=self.surface,
                       color=colour,
                       radius=INTERVAL // 2,
                       center=tuple(point),
                       )

    def draw(self, data):
        self.surface.fill((0, 0, 0))
        largest = max(data)
        smallest = min(data)

        def val_to_col(v):
            return round(255 * (v - smallest) / (largest - smallest))

        for p, v in zip(self.points, data):
            col = (255, 255-val_to_col(v), 0)
            self._draw_circle(p, col)
        pg.display.flip()

    def run(self):
        i = 0
        self.draw(self.data[i])
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    i = (i + 1) % 2
                    self.draw(self.data[i])
                    print("Drawn")


if __name__ == '__main__':
    app = CCOHeatMapDrawer()
    app.run()
