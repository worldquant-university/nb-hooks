from argparse import ArgumentParser
from typing import Optional, Sequence


def check_pip_installs(filename):
    with open(filename, "r") as f:
        text = f.read()

    if "pip install" in text:
        print(f"pip install found in: {filename}")
        print("Remove. If you need a new library installed, ask Nicholas.\n")
        return 1

    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Check filename.")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    flags = [check_pip_installs(filename) for filename in args.filenames]

    if sum(flags):
        return 1
    else:
        return 0


if __name__ == "__main__":
    exit(main())
