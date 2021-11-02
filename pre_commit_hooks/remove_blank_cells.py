import re
from argparse import ArgumentParser
from typing import Optional, Sequence

import nbformat


def remove_blank_cells(filename: str) -> int:
    """
    Reads notebook from filename. If there are blank cells in notebook,
    removes them, overwrites file, and returns 1. Otherwise, returns 0.
    """
    nb = nbformat.read(filename, as_version=4)

    cells = nb["cells"]
    blank_cell_idx = list()

    # Get index positions of blank cells
    for idx, c in enumerate(cells):
        if c["source"] == [] or re.match(r"^\s*$", c["source"]):
            blank_cell_idx.append(idx)
    if not blank_cell_idx:
        return 0
    else:
        # Create new cell list without blank cells
        cells = [c for idx, c in enumerate(cells) if idx not in blank_cell_idx]
        nb["cells"] = cells
        with open(filename, "w") as f:
            nbformat.write(nb, f)
        return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Removes blanks cells from end of notebook")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    for filename in args.filenames:
        remove_blank_cells(filename)
    return 0


if __name__ == "__main__":
    exit(main())
