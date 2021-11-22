import nbformat


def save_nb(nb, filename):
    with open(filename, "w") as f:
        nbformat.write(nb, f)


def get_source_from_file(filename):
    nb = nbformat.read(filename, as_version=4)
    return [c["source"] for c in nb["cells"]]
