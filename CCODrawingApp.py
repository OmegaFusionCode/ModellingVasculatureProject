import csv
import logging
from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt
import pygame as pg

from CCONetworkMaker import CCONetworkMaker
from LinAlg import Vec2D
from VascularDomain import CircularVascularDomain

DRAW_RADII = True
SAMPLES = 100


class CCODrawingApp:
    RADIUS = 20.0

    def __init__(self, iterations):
        pg.init()
        pg.display.set_mode((800, 800))
        self.surface = pg.display.get_surface()
        self.domain = v = CircularVascularDomain(400)
        self.maker = m = CCONetworkMaker(CCODrawingApp.RADIUS, Vec2D(400, 0), None, v)
        tree_gen = m.generate_trees(iterations)
        self.trees = ts = []
        for i, tr in enumerate(tree_gen):
            logging.info(f"Starting iteration {i + 1}")
            self.trees.append(tr)
            CCODrawingApp.write_to_file(i, tr)
        self.vessel_furthest_point = m.greatest_distance_from_vessel(ts[iterations - 1], SAMPLES)
        self.terminal_furthest_point = m.greatest_distance_from_terminal(ts[iterations - 1], SAMPLES)
        self.blackbox_counts = m.count_blackboxes(ts[iterations - 1], SAMPLES)
        logging.info(f"Vessel Furthest Point is {self.vessel_furthest_point[0]}")
        logging.info(f"Terminal Furthest Point is {self.terminal_furthest_point[0]}")

    @staticmethod
    def write_to_file(identifier, tree):
        # Store readable identifiers for each vessel
        vessel_names = {}
        for i, v in enumerate(tree.descendants):
            vessel_names[repr(v)] = f"v{i}"
        # A list of key-value pairs for the construction and reading of vessel dictionaries
        vessel_maker = [
            ("id", lambda x: vessel_names[repr(x)]),
            ("proximal point", lambda x: x.proximal_point),
            ("distal point", lambda x: x.distal_point),
            ("length", lambda x: x.length),
            ("radius", lambda x: x.radius),
            ("scaling factor", lambda x: x._s),
            ("resistance constant", lambda x: x._k_res),
            ("resistance", lambda x: x.resistance),
            ("pressure drop", lambda x: x.resistance * x.num_terminals),
            ("parent", lambda x: vessel_names[repr(x.parent)] if x.parent is not tree else None),
            ("number of terminals", lambda x: x.num_terminals),
            ("left child", lambda x: vessel_names[repr(x.children[0])] if len(x.children) > 0 else None),
            ("right child", lambda x: vessel_names[repr(x.children[1])] if len(x.children) > 0 else None),
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

    def graph(self):
        # We have pairs of points and counts.
        # We want pairs of counts and frequencies.
        frequencies = defaultdict(int)
        for _, n in self.blackbox_counts:
            frequencies[n] += 1
        # Get the range of keys in the dict
        largest_key = max(frequencies.keys())
        x_values = []
        y_values = []
        for i in range(largest_key+1):
            x_values.append(i)
            y_values.append(frequencies[i])
        plt.plot(x_values, y_values)
        plt.show()

    def draw(self, index):
        self.surface.fill((0, 0, 0))
        pg.display.flip()
        logging.info(f"Drawing state at iteration {index + 1}")
        # Draw micro-circulatory black boxes
        for v in self.trees[index].descendants:
            if len(v.children) == 0:  # I.e. vessel is a terminal
                pg.draw.circle(surface=self.surface,
                               color=(127, 0, 127),
                               radius=round(self.domain.characteristic_length(self.trees[index].num_terminals)),
                               center=tuple(v.distal_point),
                               )
        # Draw grid sample points
        for p in self.domain.point_grid(SAMPLES):
            pg.draw.circle(surface=self.surface,
                           color=(0, 0, 255),
                           radius=1,
                           center=tuple(p),
                           )
        # Draw vessels
        for v in self.trees[index].descendants:
            r = round(v.radius) if DRAW_RADII else 1
            pg.draw.line(surface=self.surface,
                         color=(255, 0, 0),
                         start_pos=tuple(v.proximal_point),
                         end_pos=tuple(v.distal_point),
                         width=r,
                         )
        _, t, p = self.terminal_furthest_point
        pg.draw.circle(surface=self.surface,
                       color=(0, 255, 0),
                       radius=5,
                       center=tuple(p),
                       )
        pg.draw.circle(surface=self.surface,
                       color=(0, 255, 0),
                       radius=5,
                       center=tuple(t),
                       )
        _, ps, p = self.vessel_furthest_point
        pg.draw.circle(surface=self.surface,
                       color=(0, 255, 255),
                       radius=5,
                       center=tuple(p),
                       )
        pg.draw.line(surface=self.surface,
                     color=(0, 255, 255),
                     width=1,
                     start_pos=ps[0],
                     end_pos=ps[1],
                     )
        pg.display.flip()

    def run(self):
        #self.graph()
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
    app = CCODrawingApp(55)
    app.run()