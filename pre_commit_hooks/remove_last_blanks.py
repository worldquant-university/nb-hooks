from argparse import ArgumentParser
from typing import Optional, Sequence

import nbformat


def remove_empty_last_cells(filename: str) -> int:
    """
    Reads notebook from filename. If there are blank cells at the
    end of the notebook, removes them, overwrites file, and returns 1.
    Otherwise, returns 0.
    """
    nb = nbformat.read(filename, as_version=4)

    cells = nb["cells"]
    start_cells = len(cells)

    while cells[-1]["source"] == "":
        cells.pop()

    if len(cells) == start_cells:
        return 0
    else:
        with open(filename, "w") as f:
            nbformat.write(nb, f)
        return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Removes blanks cells from end of notebook")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    for filename in args.filenames:
        remove_empty_last_cells(filename)
    return 0


if __name__ == "__main__":
    exit(main())
