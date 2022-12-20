from argparse import ArgumentParser
from typing import Optional, Sequence

import nbformat
from thefuzz import fuzz

from pre_commit_hooks.utils import copyright_text


def add_colophon(filename: str) -> int:
    nb = nbformat.read(filename, as_version=4)
    cells = nb["cells"]

    # Exact match in last cell
    if cells[-1]["source"] == copyright_text:
        return 0
    # Fuzzy match in last cell, replace text
    elif 50 < fuzz.ratio(cells[-1]["source"], copyright_text) < 100:
        cells[-1]["source"] = copyright_text
    # Add Markdown cell with text
    else:
        cells.append(nbformat.v4.new_markdown_cell(source=copyright_text))

    with open(filename, "w") as f:
        nbformat.write(nb, f)

    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Add copyright colophon to end of notebook.")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    for filename in args.filenames:
        add_colophon(filename)
    return 0


if __name__ == "__main__":
    exit(main())
