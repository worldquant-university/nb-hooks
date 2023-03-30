from argparse import ArgumentParser
from typing import Optional, Sequence


def sort_spelling_dict(filename):
    with open(filename, "r") as f:
        terms_old = f.readlines()
        terms_new = sorted(list(set(terms_old)))

        if terms_old != terms_new:
            f.writelines(terms_new)
            print("Sorted dictionary.")
            return 1

    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Sort dictionary.")
    parser.add_argument("filename", help="Dictionary path")
    args = parser.parse_args(argv)

    fail_flag = sort_spelling_dict(args.filename)
    return fail_flag


if __name__ == "__main__":
    exit(main())
