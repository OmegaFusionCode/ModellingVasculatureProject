from __future__ import annotations


def write_data_to_file(filepath, data, header=None):
    """Write a 2D array of result values to a specified filepath with tab-separated values. """
    with open(f"results/{filepath}", mode="w") as f:
        if header is not None:
            f.write("\t".join((field for field in header)) + "\n")
        f.write("\n".join(("\t".join((str(datum) for datum in row))) for row in data))


def concat(xs):
    return [y for x in xs for y in x]