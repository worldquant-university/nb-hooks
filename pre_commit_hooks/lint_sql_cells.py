from argparse import ArgumentParser
from typing import Optional, Sequence

import nbformat
import sqlparse


def clean_sql_string(source: str) -> str:
    source = source.strip("%%sql").strip("\n")
    source = sqlparse.format(
        source,
        reindent=True,
        use_space_around_operators=True,
        keyword_case="upper",
        reindent_aligned=False,
        identifier_case="lower",
    )
    if source[-11:] == " -- REMOVE}":
        source = source.replace(" -- REMOVE}", "\n-- REMOVE}")
    source = ("%%sql\n" + source).replace("\n\n", "\n")
    return source


def clean_sql_cells(filename: str) -> int:
    nb = nbformat.read(filename, as_version=4)
    cells = nb["cells"]
    fail_flag = 0
    for cell in cells:
        if (cell["cell_type"] == "code") and ("%%sql" in cell["source"]):
            clean_code = clean_sql_string(cell["source"])
            if cell["source"] != clean_code:
                cell["source"] = clean_sql_string(cell["source"]).replace("\n\n", "\n")
                fail_flag = 1
    if fail_flag == 1:
        with open(filename, "w") as f:
            nbformat.write(nb, f)
        return 1
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Lint notebook cells starting with '%%sql'")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    for filename in args.filenames:
        clean_sql_cells(filename)
    return 0


if __name__ == "__main__":
    exit(main())
