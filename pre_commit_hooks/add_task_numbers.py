import os
import re
from argparse import ArgumentParser
from typing import Optional, Sequence

import nbformat


def add_task_numbers(filename: str) -> int:
    # Get notebook number or skip NB if none
    nb_basename = os.path.basename(filename)
    try:
        nb_num = int(nb_basename.split("-")[0])
    except ValueError:
        return 0

    # Read in notebook
    nb = nbformat.read(filename, as_version=4)

    fail_flag = 0
    task_num = 1

    regex_pattern = re.compile(r"\*\*Task.*?\*\*")

    # Iterate through notebook cells
    for c in nb["cells"]:
        if c["cell_type"] == "markdown":
            # Check if there's a task in cell
            if "**Task" in c["source"]:
                task_pattern = f"**Task {nb_num}.{task_num}:**"
                # Check if task's correctly numbered
                if task_pattern not in c["source"]:
                    # Correct number
                    c["source"] = re.sub(regex_pattern, task_pattern, c["source"])
                    fail_flag = 1
                task_num += 1

    if fail_flag == 1:
        with open(filename, "w") as f:
            nbformat.write(nb, f)

    return fail_flag


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Adds or corrects task numbering")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    for filename in args.filenames:
        add_task_numbers(filename)
    return 0


if __name__ == "__main__":
    exit(main())
