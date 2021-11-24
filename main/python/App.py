import logging
from datetime import datetime

import pygame as pg

from CCONetworkBuilder import CCONetworkBuilder
from LinAlg import Vec2D
from VascularDomain import RectangularVascularDomain, CircularVascularDomain


class App:

    def __init__(self, iterations):
        pg.init()
        pg.display.set_mode((800, 800))
        self.surface = pg.display.get_surface()
        self.domain = v = CircularVascularDomain(40)
        self.builder = b = CCONetworkBuilder(1, Vec2D(40, 0), None, v)
        tree_gen = b.generate_trees(iterations)
        self.trees = []
        for i, tr in enumerate(tree_gen):
            logging.info(f"Starting iteration {i+1}")
            self.trees.append(tr)

    def draw(self, index):
        self.surface.fill((0, 0, 0))
        logging.info(f"Drawing state at iteration {index+1}")
        for v in self.trees[index].vessels:
            # print(f"Vessel with radius {v.radius} at {v.proximal_point}, {v.distal_point}")
            pg.draw.line(surface=self.surface,
                         color=(255, 0, 0),
                         start_pos=tuple(v.proximal_point * 10),
                         end_pos=tuple(v.distal_point * 10),
                         width=round(v.radius),
                         )
        pg.display.flip()

    def run(self):
        self.draw(i := 0)
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT and i > 0:
                        self.draw(i := i-1)
                    if event.key == pg.K_RIGHT and i + 1 < len(self.trees):
                        self.draw(i := i+1)


if __name__ == '__main__':
    # Set up the logger and enable printing to the console.
    dt = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    print(dt)
    logging.basicConfig(filename=f"./logs/{dt}.log",
                        filemode="w",
                        level=logging.DEBUG,
                        )
    logging.getLogger().addHandler(logging.StreamHandler())
    app = App(200)
    app.run()
