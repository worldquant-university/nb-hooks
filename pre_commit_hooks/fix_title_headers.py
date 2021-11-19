from argparse import ArgumentParser
from typing import Optional, Sequence


def check_for_title(filename):
    pass


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Fixes notebook titles and H1 headers")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    for filename in args.filenames:
        check_for_title(filename)
    return 0


if __name__ == "__main__":
    exit(main())
