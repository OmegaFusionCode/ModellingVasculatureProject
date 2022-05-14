import csv

from BarChartPlotter import BarChartPlotter


def plot_data(data):
    plotter = BarChartPlotter(data)
    plotter.plot()


def get_terminal_data():
    full = _get_ith_entry_data("results", i=2)
    dead_ends = _get_ith_entry_data("results", i=3)
    shortest_path = _get_ith_entry_data("results", i=4)
    return full, dead_ends, shortest_path


def _get_ith_entry_data(filename, i=2):
    data = []
    with open(f"results/percolation/{filename}.txt") as tsv:
        first_line = True
        for line in csv.reader(tsv, delimiter="\t"):
            if first_line:
                first_line = False
                continue
            data.append(int(line[i-1]))
    return data


if __name__ == "__main__":
    f, d, s = get_terminal_data()
    print(f)
    print(d)
    print(s)
    plot_data(f)
    plot_data(d)
    plot_data(s)
