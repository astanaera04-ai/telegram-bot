import sys
import os


def read_logs(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} does not exist.", file=sys.stderr)
        return

    with open(filepath, 'r') as file:
        for line in file:
            yield line.strip()