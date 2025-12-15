import sys
from pathlib import Path


def get_last_10_lines_from_file(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    with path.open('r', encoding='utf-8', errors='replace') as file:
        last_10_lines = file.read().splitlines()[-10:]
    return last_10_lines


def get_last_17_lines_from_stdin():
    data = sys.stdin.read()
    last_17_lines = data.splitlines()[-17:]
    return last_17_lines


def get_name_with_last_N_lines():
    files_with_last_lines = {}
    args = sys.argv[1:]
    if len(args) > 0:
        for file in args:
            path = Path(file)
            last_lines = get_last_10_lines_from_file(path)
            files_with_last_lines[str(path)] = last_lines
    else:
        last_lines = get_last_17_lines_from_stdin()
        files_with_last_lines[""] = last_lines
    return files_with_last_lines


def print_last_lines(files_with_last_lines: dict):
    for key, value in files_with_last_lines.items():
        if key != "":
            print(f"==> {key} <==")
        for line in value:
            print(line)


def main():
    try:
        files_with_last_lines = get_name_with_last_N_lines()
        print_last_lines(files_with_last_lines)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()