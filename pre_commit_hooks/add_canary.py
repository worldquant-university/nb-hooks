import random
from argparse import ArgumentParser
from typing import Optional, Sequence

import nbformat
from nbformat.notebooknode import NotebookNode

from pre_commit_hooks.utils import canary_text


def read_nb(filename: str) -> NotebookNode:
    nb = nbformat.read(filename, as_version=4)
    return nb


def add_canary(filename: str) -> int:
    with open(filename, "r") as f:
        text = f.read()

    if canary_text in text:
        return 0

    nb = read_nb(filename)
    cells = nb["cells"]

    # Filter cells to just MD
    md_cells = [
        (idx, c)
        for (idx, c) in enumerate(cells[2:], start=2)  # 2 b/c title and usage cells
        if (cells[idx]["cell_type"] == "markdown")
        and not (cells[idx]["source"].startswith("#"))
    ]

    idx, _ = random.choice(md_cells)
    cells[idx]["source"] += canary_text

    with open(filename, "w") as f:
        nbformat.write(nb, f)

    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Add invisible text to random MD cell.")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    fail_flag = 0
    for filename in args.filenames:
        if add_canary(filename) == 1:
            fail_flag = 1
    return fail_flag


if __name__ == "__main__":
    exit(main())
