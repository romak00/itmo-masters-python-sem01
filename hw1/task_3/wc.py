import sys
from pathlib import Path


def get_counters_from_str(data: str):
    lines_count = data.count('\n')
    words_count = len(data.split())
    chars_count = len(data.encode('utf-8'))
    return lines_count, words_count, chars_count


def get_counters_from_file(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    with path.open('r', encoding='utf-8', errors='replace') as file:
        data = file.read()
        lc, wc, cc = get_counters_from_str(data)
    return lc, wc, cc, str(path)


def get_counters_from_stdin():
    data = sys.stdin.read()
    lc, wc, cc = get_counters_from_str(data)
    return lc, wc, cc, ""


def collect_counters():
    counters = []
    args = sys.argv[1:]
    if len(args) > 0:
        for file in args:
            path = Path(file)
            counters.append(get_counters_from_file(path))
    else:
        counters.append(get_counters_from_stdin())
    return counters


def print_counters(counters: list):
    NUM_WIDTH = 4
    total_lc, total_wc, total_cc = 0, 0, 0
    for entry in counters:
        lc, wc, cc, fn = entry
        print(f"{str(lc).rjust(NUM_WIDTH)} {str(wc).rjust(NUM_WIDTH)} {str(cc).rjust(NUM_WIDTH)} {fn}")
        total_lc += lc
        total_wc += wc
        total_cc += cc
    if (len(counters) > 1):
        print(f"{str(total_lc).rjust(NUM_WIDTH)} {str(total_wc).rjust(NUM_WIDTH)} {str(total_cc).rjust(NUM_WIDTH)} total")


def main():
    try:
        counters = collect_counters()
        print_counters(counters)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()