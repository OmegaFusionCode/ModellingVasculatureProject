import pygame as pg

from BloodVessel import BloodVessel
from VascularTree import VascularTree

SCREEN_X = 1024
SCREEN_Y = 640


class App:

    def __init__(self):
        self.__running = False
        self.__display_surf = None
        self.size = self.weight, self.height = 640, 400

    def on_init(self):
        pg.init()
        self.__display_surf = pg.display.set_mode(self.size, pg.HWSURFACE | pg.DOUBLEBUF)
        self.__running = True
        self.__background = pg.Surface(self.__display_surf.get_size()).convert()

    def draw_vascular_tree(self, tree: VascularTree) -> None:
        vessels = tree.vessels
        objects = [pg.rect]

    def on_execute(self) -> None:
        if self.on_init() is False:
            self.__running = False
        else:
            self.draw_network()
        while self.__running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False
        pg.quit()


if __name__ == '__main__':
    app = App()
    app.on_execute()
