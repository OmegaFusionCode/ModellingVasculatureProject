import matplotlib.pyplot as plt

from CCONetworkMaker import CCONetworkMaker
from LinAlg import Vec2D
from VascularDomain import CircularVascularDomain


DRAW_RADII = True


class GraphingApp:

    RADIUS = 20.0
    MEASURE_DIST = False

    def __init__(self, iterations):
        self.domain = v = CircularVascularDomain(400)
        self.iterations = iterations

    def run(self, number_of_points):
        for i in range(number_of_points):
            maker = CCONetworkMaker(GraphingApp.RADIUS, Vec2D(400, 0), None, self.domain)
            print(f"Generating tree {i}")
            tree_gen = maker.generate_trees(self.iterations)
            try:
                for _ in tree_gen: continue  # Consume the generator#
            except AssertionError:
                print("Assertion failed. Skipping...")
                continue
            arr = maker.iter_num_with_dist if GraphingApp.MEASURE_DIST else maker.iter_num_with_depth
            x_values = []
            y_values = []
            for (x, y) in arr:
                x_values.append(x)
                y_values.append(y)
            plt.plot(x_values, y_values)
        plt.show()


if __name__ == '__main__':
    app = GraphingApp(25)
    app.run(15)
