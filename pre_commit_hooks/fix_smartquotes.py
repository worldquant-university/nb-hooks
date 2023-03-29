from argparse import ArgumentParser
from typing import Optional, Sequence


def fix_smartquotes(filename):
    sm_dict = {"“": '"', "”": '"', "‘": "'", "’": "'"}

    with open(filename, "r") as f:
        text = f.read()

    fail_flag = 0

    for key, val in sm_dict.items():
        if key in text:
            text = text.replace(key, val)
            fail_flag += 1

    if fail_flag:
        with open(filename, "w") as f:
            f.write(text)
        return 1
    else:
        return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Check filename.")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    flags = [fix_smartquotes(filename) for filename in args.filenames]

    if sum(flags):
        return 1
    else:
        return 0


if __name__ == "__main__":
    exit(main())
