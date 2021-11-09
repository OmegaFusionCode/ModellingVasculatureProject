import pygame as pg

from CCONetworkBuilder import CCONetworkBuilder
from LinAlg import Vec2D
from VascularDomain import RectangularVascularDomain


def main():
    pg.init()
    pg.display.set_mode((750, 750))
    surface = pg.display.get_surface()

    v = RectangularVascularDomain(75, 75)
    b = CCONetworkBuilder(1, Vec2D(37.5, 75.0), None, v)
    t = b.run(65)
    for v in t.vessels:
        print(f"Vessel with radius {v.radius} at {v.proximal_point}, {v.distal_point}")
        pg.draw.line(surface, (255, 0, 0), tuple(v.proximal_point * 10), tuple(v.distal_point * 10))

    pg.display.flip()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                running = False


if __name__ == '__main__':
    main()
