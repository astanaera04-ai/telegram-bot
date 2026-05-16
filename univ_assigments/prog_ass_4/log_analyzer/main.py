import sys
import os

# Python-ға қазіргі папкадан (log_analyzer ішінен) модульдерді іздеуді бұйырамыз
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parser import parse_line
from reader import read_logs
from filters import ErrorIterator
from decorators import log_call, timer


@log_call
@timer
def analyze(filepath):
    lines = list(read_logs(filepath))

    total_lines = len(lines)
    error_count = 0
    unique_ips = set()

    for err_line in ErrorIterator(lines):
        parsed = parse_line(err_line)
        if parsed:
            error_count += 1
            unique_ips.add(parsed['ip'])

    print("\n--- Summary Report ---")
    print(f"Total lines: {total_lines}")
    print(f"Number of ERRORs: {error_count}")
    print(f"Unique IPs causing errors: {', '.join(unique_ips)}")


if __name__ == "__main__":
    import os

    # main.py тұрған папканы табамыз
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # sample.log файлы осы папканың ішінде тұрғанын көрсетеміз
    log_file_path = os.path.join(current_dir, "sample.log")

    analyze(log_file_path)