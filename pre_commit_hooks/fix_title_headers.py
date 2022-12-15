import os
from argparse import ArgumentParser
from typing import Optional, Sequence

import nbformat
from nbformat.notebooknode import NotebookNode


def read_nb(filename: str) -> NotebookNode:
    nb = nbformat.read(filename, as_version=4)
    return nb


def check_for_title(filename: str) -> int:
    nb = read_nb(filename)
    nb_basename = os.path.basename(filename)
    second_cell = nb["cells"][1]

    # Check that first cell is Markdown
    if second_cell["cell_type"] != "markdown":
        print(f"{nb_basename}: Missing title.")
        return 1

    # Check that first cell starts w/ proper title formatting
    if second_cell["source"][:24] != '<font size="+3"><strong>':
        print(
            f'{nb_basename}: Missing title formatting tags (`<font size="+3"><strong>`).'
        )
        return 1

    # Check that first cell only contains title, check by tags
    if second_cell["source"][-16:] != "</strong></font>":
        print(f"{nb_basename}: Additional text in title cell.")
        return 1

    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Fixes notebook titles and H1 headers")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    fail_flag = 0
    for filename in args.filenames:
        if check_for_title(filename) == 1:
            fail_flag = 1
    return fail_flag


if __name__ == "__main__":
    exit(main())
