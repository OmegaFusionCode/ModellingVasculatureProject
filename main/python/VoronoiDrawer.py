import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, Delaunay, voronoi_plot_2d, delaunay_plot_2d


if __name__ == "__main__":
    rng = np.random.default_rng()
    points = rng.random((100, 2))
    vor = Voronoi(points)
    de = Delaunay(points)

    _ = voronoi_plot_2d(vor)
    _ = delaunay_plot_2d(de)
    plt.show()
