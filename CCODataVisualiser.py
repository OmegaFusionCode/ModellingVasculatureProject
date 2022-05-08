import csv

from BarChartPlotter import BarChartPlotter
from HistogramPlotter import HistogramPlotter


def plot_data(d):
    #  we want 20 times as many data values as bins
    plotter = HistogramPlotter(d, len(d) // 20)
    plotter.plot()


def plot_discrete_data(d):
    plotter = BarChartPlotter(d)
    plotter.plot()


def get_terminal_data():
    return _get_second_entry_data("terminal")


def get_vessel_data():
    return _get_second_entry_data("vessel")


def get_blackbox_data():
    return _get_second_entry_data("blackboxes")


def _get_second_entry_data(filename):
    data = []
    with open(f"results/cco/{filename}.txt") as tsv:
        first_line = True
        for line in csv.reader(tsv, delimiter="\t"):
            if first_line:
                first_line = False
                continue
            data.append(float(line[1]))
    return data


if __name__ == "__main__":
    t = get_terminal_data()
    v = get_vessel_data()
    b = [int(n) for n in get_blackbox_data()]
    print(t)
    print(v)
    plot_data(t)
    plot_data(v)
    plot_discrete_data(b)
