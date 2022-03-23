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
SAMPLES = 5
GLOBAL_RADIUS = 400


def write_data_to_file(filepath, data, header=None):
    """Write a 2D array of result values to a specified filepath with tab-separated values. """
    with open(f"results/cco-results/{filepath}", mode="w") as f:
        if header is not None:
            f.write("\t".join((field for field in header)) + "\n")
        f.write("\n".join(("\t".join((str(datum) for datum in row))) for row in data))


class CCODrawingApp:
    RADIUS = 20.0

    def __init__(self, iterations):
        pg.init()
        pg.display.set_mode((GLOBAL_RADIUS*2, GLOBAL_RADIUS*2))
        self.surface = pg.display.get_surface()
        self.domain = v = CircularVascularDomain(GLOBAL_RADIUS)
        self.maker = m = CCONetworkMaker(CCODrawingApp.RADIUS, Vec2D(400, 0), None, v)
        tree_gen = m.generate_trees(iterations)
        self.trees = ts = []
        for i, tr in enumerate(tree_gen):
            logging.info(f"Starting iteration {i + 1}")
            self.trees.append(tr)
            CCODrawingApp.write_pressures_flows_to_file(i, tr)
        self.vessel_furthest_point = m.greatest_distance_from_vessel(ts[iterations - 1], SAMPLES)
        self.terminal_furthest_point = m.greatest_distance_from_terminal(ts[iterations - 1], SAMPLES)
        self.blackbox_counts = m.count_blackboxes(ts[iterations - 1], SAMPLES)
        logging.info(f"Vessel Furthest Point is {self.vessel_furthest_point[0]}")
        logging.info(f"Terminal Furthest Point is {self.terminal_furthest_point[0]}")
        self.compute_sample_point_distances(list(v.point_grid(SAMPLES)))

    def compute_sample_point_distances(self, sample_points):
        """For the final tree, record the distances to and from each point in a file"""
        t = self.trees[-1]  # The final tree
        vessel_furthest_points = {s: self.maker.distance_from_vessel(t, s) for s in sample_points}
        terminal_furthest_points = {s: self.maker.distance_from_terminal(t, s) for s in sample_points}
        print(vessel_furthest_points)
        print(terminal_furthest_points)
        vessel_data = ((a, b, c) for a, (b, c) in vessel_furthest_points.items())
        write_data_to_file("vessel.txt", vessel_data, ("Point", "Distance", "Start and End Point"))
        terminal_data = ((a, b, c) for a, (b, c) in terminal_furthest_points.items())
        write_data_to_file("terminal.txt", terminal_data, ("Point", "Distance", "Terminal"))
        return vessel_furthest_points, terminal_furthest_points

    @staticmethod
    def write_pressures_flows_to_file(identifier, tree):
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

    def _draw_circles(self, points, radius, colour):
        for p in points:
            pg.draw.circle(surface=self.surface,
                           color=colour,
                           radius=radius,
                           center=tuple(p),
                           )

    def draw(self, index):
        self.surface.fill((0, 0, 0))
        pg.display.flip()
        logging.info(f"Drawing state at iteration {index + 1}")
        # Draw micro-circulatory black boxes
        #for v in self.trees[index].descendants:
        #    if len(v.children) == 0:  # I.e. vessel is a terminal
        #        pg.draw.circle(surface=self.surface,
        #                       color=(127, 0, 127),
        #                       radius=round(self.domain.characteristic_length(self.trees[index].num_terminals)),
        #                       center=tuple(v.distal_point),
        #                       )
        # Draw grid sample points
        self._draw_circles(self.domain.point_grid(SAMPLES),
                           1,
                           (0, 0, 255)
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
        self._draw_circles((p, t),
                           radius=5,
                           colour=(0, 255, 0))
        _, ps, p = self.vessel_furthest_point
        self._draw_circles((p,),
                           radius=5,
                           colour=(0, 255, 255))
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
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print(pg.mouse.get_pos())


if __name__ == '__main__':
    # Set up the logger and enable printing to the console.
    dt = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    print(dt)
    logging.basicConfig(filename=f"./logs/{dt}.log",
                        filemode="w",
                        level=logging.DEBUG,
                        )
    logging.getLogger().addHandler(logging.StreamHandler())
    app = CCODrawingApp(3)
    app.run()
