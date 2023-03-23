import os
from argparse import ArgumentParser
from typing import Optional, Sequence


def fix_filename(filename):
    if filename[-6:] != ".ipynb":
        return 1
    head, tail = os.path.split(filename)
    head_dirs = head.split("/")

    if len(head_dirs) != 4:
        head_passing = False
    elif head_dirs[0] != "python-materials":
        head_passing = False
    elif "module" not in head_dirs[2]:
        head_passing = False
    elif "lesson" not in head_dirs[3]:
        head_passing = False
    else:
        head_passing = True

    if not head_passing:
        print(
            "Course note filepaths must be:",
            "'python-materials/<course-name>/module-<x>/lesson-<x>/course_name_module_<x>_lesson_<x>.ipynb'",
        )
        return 1

    new_tail = (
        head_dirs[1].replace("-", "_")
        + "_module_"
        + head_dirs[2][-1]
        + "_lesson_"
        + head_dirs[3][-1]
        + ".ipynb"
    )

    if tail != new_tail:
        os.rename(filename, os.path.join(head, new_tail))
        print(f"Renaming '{tail}' -> '{new_tail}'.")
        return 1

    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Add copyright colophon to end of notebook.")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    for filename in args.filenames:
        fix_filename(filename)
    return 0


if __name__ == "__main__":
    exit(main())
