import tkinter as tk
from tkinter import ttk
from threading import Thread

import time

from DrawingApp import DrawingApp


#class AppRunner(Thread):
#
#    def __init__(self, iterations):
#        super().__init__()
#        self.iterations = iterations
#
#    def run(self):
#        app = App(self.iterations)
#        app.run()

class AsyncButtonClick(Thread):

    def __init__(self, iterations):
        super().__init__()
        self.drawing_app = DrawingApp(iterations)

    def run(self):
        print("Clicked!")
        self.drawing_app.run()
        print("Finished!")


class TkApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Tkinter Demo")
        self.geometry("600x400")

        self.iterations_var = tk.IntVar()
        iterations_entry = ttk.Entry(self, textvariable=self.iterations_var)
        iterations_entry.pack()

        button = ttk.Button(self, text="Click me!", command=self.button_clicked)
        button.pack()

    def button_clicked(self):
        iterations = self.iterations_var.get()
        if iterations:
            click_thread = AsyncButtonClick(iterations)
            click_thread.start()

            self.monitor(click_thread)

    def monitor(self, thread):
        if thread.is_alive():
            self.after(100, lambda: self.monitor(thread))


if __name__ == "__main__":
    app = TkApp()
    app.mainloop()
