import numpy as np
from matplotlib import pyplot as plt


class HistogramPlotter:

    def __init__(self, data, bins):
        self.data = data
        self.bins = bins

    def plot(self):
        smallest = min(self.data)
        largest = max(self.data)
        plt.hist(self.data, bins=self.bins, edgecolor="black")
        plt.show()


if __name__ == "__main__":
    x = np.random.random_integers(1, 100, 5)
    print(x)
    plt.hist(x, bins=20)
    plt.show()