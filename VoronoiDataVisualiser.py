import csv

from HistogramPlotter import HistogramPlotter


def plot_data(d):
    plotter = HistogramPlotter(d, len(d) // 10)
    plotter.plot()


def get_data():
    data = []
    with open(f"results/voronoi/results.txt") as tsv:
        first_line = True
        for line in csv.reader(tsv, delimiter="\t"):
            if first_line:
                first_line = False
                continue
            data.append(float(line[1]))
    return data


if __name__ == "__main__":
    d = get_data()
    print(d)
    plot_data(d)