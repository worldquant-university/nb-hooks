import os
from argparse import ArgumentParser
from typing import Optional, Sequence


def check_filename(filename):
    if filename[-6:] != ".ipynb":
        return 0
    head, tail = os.path.split(filename)

    # Catch notebooks not in correct subdirectories
    try:
        _, course, module, lesson = head.split("/")
    except ValueError:
        print(f"Filepath incorrect for: {filename}.")
        print(
            "Doesn't match pattern :",
            "python-materials/<course-name>/module-<x>/lesson-<y>/course_name_module_<x>_lesson_<y>.ipynb",
        )
        print("Make sure notebook is in correct directory.\n")
        return 1

    # Catch notebooks with wrong name
    course_abbr = "_".join(course.split("-")[:2])

    correct_tail = (
        course_abbr + "_module_" + module[-1] + "_lesson_" + lesson[-1] + ".ipynb"
    )

    if tail != correct_tail:
        print(f"Filename incorrect for: {tail}.")
        print(f"Doesn't match pattern : {correct_tail}.")
        print("Rename and recommit.\n")
        return 1

    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Check filename.")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    flags = [check_filename(filename) for filename in args.filenames]

    if sum(flags):
        return 1
    else:
        return 0


if __name__ == "__main__":
    exit(main())
