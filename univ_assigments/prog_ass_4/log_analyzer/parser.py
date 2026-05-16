import re

def parse_line(line):
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(?P<level>INFO|WARNING|ERROR)\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+-\s+(?P<message>.*)'
    match = re.search(pattern, line)
    if match:
        return match.groupdict()
    return None