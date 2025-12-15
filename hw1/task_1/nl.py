import sys
from pathlib import Path


def get_lines_from_file(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    with path.open('r', encoding='utf-8', errors='replace') as file:
        lines = file.read().splitlines()
    return lines


def get_lines_from_stdin():
    data = sys.stdin.read()
    lines = data.splitlines()
    return lines


def get_lines():
    args = sys.argv[1:]
    if len(args) > 0:
        path = Path(args[0])
        lines = get_lines_from_file(path)
    else:
        lines = get_lines_from_stdin()
    return lines


def print_enum_lines(lines: list[str]):
    NUM_WIDTH = 6
    for i, line in enumerate(lines, start=1):
        num_field = str(i).rjust(NUM_WIDTH)
        print(f"{num_field}\t{line}")


def main():
    try:
        lines = get_lines()
        print_enum_lines(lines)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()