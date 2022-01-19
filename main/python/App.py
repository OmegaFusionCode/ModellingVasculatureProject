import csv
import logging
from datetime import datetime

import pygame as pg

from CCONetworkMaker import CCONetworkMaker
from LinAlg import Vec2D
from VascularDomain import CircularVascularDomain


class App:

    RADIUS = 20.0

    def __init__(self, iterations):
        pg.init()
        pg.display.set_mode((800, 800))
        self.surface = pg.display.get_surface()
        self.domain = v = CircularVascularDomain(400)
        self.maker = m = CCONetworkMaker(App.RADIUS, Vec2D(400, 0), None, v)
        tree_gen = m.generate_trees(iterations)
        self.trees = []
        for i, tr in enumerate(tree_gen):
            logging.info(f"Starting iteration {i + 1}")
            self.trees.append(tr)
            App.write_to_file(i, tr)

    @staticmethod
    def write_to_file(identifier, tree):
        # Store readable identifiers for each vessel
        vessel_names = {}
        for i, v in enumerate(tree.descendants):
            vessel_names[repr(v)] = f"v{i}"
        # A list of key-value pairs for the construction and reading of vessel dictionaries
        vessel_maker = [
            ("id", lambda v: vessel_names[repr(v)]),
            ("proximal point", lambda v: v.proximal_point),
            ("distal point", lambda v: v.distal_point),
            ("length", lambda v: v.length),
            ("radius", lambda v: v.radius),
            ("scaling factor", lambda v: v._s),
            ("resistance constant", lambda v: v._k_res),
            ("resistance", lambda v: v.resistance),
            ("pressure drop", lambda v: v.resistance * v.num_terminals),
            ("parent", lambda v: vessel_names[repr(v.parent)] if v.parent is not tree else None),
            ("number of terminals", lambda v: v.num_terminals),
            ("left child", lambda v: vessel_names[repr(v.children[0])] if len(v.children) > 0 else None),
            ("right child", lambda v: vessel_names[repr(v.children[1])] if len(v.children) > 0 else None),
        ]
        vessels = []
        for v in tree.descendants:
            this_vessel = {}
            for k, f in vessel_maker:
                this_vessel[k] = str(f(v))
            vessels.append(this_vessel)
        with open(f"results/results{identifier}.txt", mode="w", newline="") as f:
            my_writer = csv.DictWriter(f, delimiter="\t", fieldnames=[t[0] for t in vessel_maker])
            my_writer.writeheader()
            my_writer.writerows(vessels)

    def draw(self, index):
        self.surface.fill((0, 0, 0))
        pg.display.flip()
        logging.info(f"Drawing state at iteration {index + 1}")
        for v in self.trees[index].descendants:
            pg.draw.line(surface=self.surface,
                         color=(255, 0, 0),
                         start_pos=tuple(v.proximal_point),
                         end_pos=tuple(v.distal_point),
                         width=round(v.radius),
                         )
        pg.display.flip()

    def run(self):
        self.draw(i := 0)
        running = True
        n = len(self.trees) - 1
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT and i > 0:
                        self.draw(i := i - 1)
                    if event.key == pg.K_RIGHT and i < n:
                        self.draw(i := i + 1)
                    if event.key == pg.K_DOWN:
                        self.draw(i := 0)
                    if event.key == pg.K_UP:
                        self.draw(i := n)


if __name__ == '__main__':
    # Set up the logger and enable printing to the console.
    dt = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    print(dt)
    logging.basicConfig(filename=f"./logs/{dt}.log",
                        filemode="w",
                        level=logging.DEBUG,
                        )
    logging.getLogger().addHandler(logging.StreamHandler())
    app = App(50)
    app.run()
