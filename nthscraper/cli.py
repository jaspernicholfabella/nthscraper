import os
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="NthScraper CLI tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    init_parser = subparsers.add_parser(
        "init", help="Initialize the nthscraper project in the current directory"
    )
    init_parser.set_defaults(func=create_project)

    # Parse the arguments
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func()


def create_project():
    files_to_create = ["file1.txt", "file2.txt", "file3.txt"]

    for filename in files_to_create:
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, "w") as f:
            f.write(f"Content of {filename}")
        print(f"Created file: {filepath}")


if __name__ == "__main__":
    main()
