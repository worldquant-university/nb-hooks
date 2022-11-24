import re
from argparse import ArgumentParser
from typing import Optional, Sequence

import nbformat
import sqlparse


def clean_sql_string(source: str) -> str:
    """
    Takes string from notebook cell source. Parses and lints string.
    """
    # Remove first line
    source_split = source.splitlines()
    header = source_split[0]
    body = source_split[1:]
    new_body = sqlparse.format(
        "\n".join(body),
        reindent=True,
        use_space_around_operators=True,
        keyword_case="upper",
        reindent_aligned=False,
        identifier_case="lower",
    )

    new_body = new_body.replace("-- REMOVE{\n", "-- REMOVE{").replace(
        " -- REMOVE}", "\n-- REMOVE}"
    )

    new_source = header + "\n\n\n" + new_body
    return new_source


def clean_sql_cells(filename: str) -> int:
    """
    Takes notebook filename. Reads in file, cleans all cells that begin with `"%%sql"`.
    """
    nb = nbformat.read(filename, as_version=4)
    cells = nb["cells"]
    fail_flag = 0

    regex = re.compile(r"%%sql|%%bigquery")
    for cell in cells:
        if (cell["cell_type"] == "code") and regex.match(cell["source"]):
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
