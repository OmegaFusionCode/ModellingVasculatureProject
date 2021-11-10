import pygame as pg

from CCONetworkBuilder import CCONetworkBuilder
from LinAlg import Vec2D
from VascularDomain import RectangularVascularDomain


class App:

    def __init__(self, iterations):
        pg.init()
        pg.display.set_mode((750, 750))
        self.surface = pg.display.get_surface()
        self.domain = v = RectangularVascularDomain(75, 75)
        self.builder = b = CCONetworkBuilder(1, Vec2D(37.5, 0), None, v)
        tree_gen = b.generate_trees(iterations)
        self.trees = []
        print("Starting iteration ", end="")
        for i, tr in enumerate(tree_gen):
            print(i+1, end=" ")
            self.trees.append(tr)
        print()

    def draw(self, index):
        self.surface.fill((0, 0, 0))
        print(f"Drawing state at iteration {index+1}")
        for v in self.trees[index].vessels:
            # print(f"Vessel with radius {v.radius} at {v.proximal_point}, {v.distal_point}")
            pg.draw.line(self.surface, (255, 0, 0), tuple(v.proximal_point * 10), tuple(v.distal_point * 10))
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
    app = App(65)
    app.run()
