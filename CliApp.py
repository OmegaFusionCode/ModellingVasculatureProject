from datetime import datetime
import logging

from DrawingApp import DrawingApp


class CliApp:

    def __init__(self):
        self.drawer = None

    def make_drawer(self):
        try:
            iters = int(input("Please enter number of iterations: "))
            self.drawer = DrawingApp(iters)
        except TypeError:
            print("Invalid value entered. Aborting...")

    def enable_logging(self, logging_level):
        dt = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        logging.basicConfig(filename=f"./logs/{dt}.log",
                            filemode="w",
                            level=logging_level,
                            )
        logging.getLogger().addHandler(logging.StreamHandler())

    def run(self):
        self.make_drawer()
        if self.drawer is not None:
            self.drawer.run()


if __name__ == "__main__":
    app = CliApp()
    app.enable_logging(logging.DEBUG)
    app.run()