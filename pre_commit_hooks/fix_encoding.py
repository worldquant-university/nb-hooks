import os
from argparse import ArgumentParser
from typing import Optional, Sequence


def fix_encoding(filename: str) -> int:
    try:
        with open(filename, "r", encoding="cp1252") as f:
            doc = f.read()

        os.remove(filename)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(doc)
    except:  # noQA E722
        raise Exception(f"Can't read {filename}. Not encoded in utf-8 or cp1252.")

    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = ArgumentParser("Enforce utf-8 encoding.")
    parser.add_argument("filenames", nargs="*", help="Filenames for format")
    args = parser.parse_args(argv)

    for filename in args.filenames:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                f.read()
        except UnicodeDecodeError:
            fix_encoding(filename)
    return 0


if __name__ == "__main__":
    exit(main())
