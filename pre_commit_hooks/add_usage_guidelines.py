from argparse import ArgumentParser
from typing import Optional, Sequence

import nbformat
from thefuzz import fuzz

from pre_commit_hooks.utils import piracy_warning


def add_guidelines(filename: str) -> int:
    nb = nbformat.read(filename, as_version=4)
    cells = nb["cells"]

    if "011-tabular-and-tidy-data" in filename:
        idx = 1
    else:
        idx = 0

    # Exact match in first cell: Pass
    if cells[idx]["source"] == piracy_warning:
        return 0
    # Fuzz match: Edit cell
    elif 75 < fuzz.ratio(cells[idx]["source"], piracy_warning) < 100:
        cells[idx]["source"] = piracy_warning
    # No match (i.e. cell is missing entirely), prepend
    else:
        cells.insert(idx, nbformat.v4.new_markdown_cell(source=piracy_warning))

    with open(filename, "w") as f:
        nbformat.write(nb, f)

    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Add usage guidelines at start of notebook.")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    for filename in args.filenames:
        add_guidelines(filename)
    return 0


if __name__ == "__main__":
    exit(main())
