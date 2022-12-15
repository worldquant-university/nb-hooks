from argparse import ArgumentParser
from typing import Optional, Sequence

import nbformat

from pre_commit_hooks.utils import piracy_warning


def add_guidelines(filename: str) -> int:
    nb = nbformat.read(filename, as_version=4)
    cells = nb["cells"]

    # Exact match in last cell
    if cells[0]["source"] == piracy_warning:
        return 0
    # Add Markdown cell with text
    else:
        cells.insert(0, nbformat.v4.new_markdown_cell(source=piracy_warning))

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
