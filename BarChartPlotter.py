import numpy as np
from matplotlib import pyplot as plt


class BarChartPlotter:

    def __init__(self, data):
        self.data = data

    def plot(self):
        freqs = [0 for _ in range(max(self.data)+1)]
        print(max(self.data))
        for i in self.data:
            print(i)
            freqs[i] += 1
        plt.bar(range(len(freqs)), freqs, edgecolor="black")
        plt.show()


if __name__ == "__main__":
    x = np.random.random_integers(1, 10, 5)
    print(x)
    plotter = BarChartPlotter(x)
    plotter.plot()