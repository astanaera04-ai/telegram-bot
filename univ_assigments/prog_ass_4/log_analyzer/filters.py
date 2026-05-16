class ErrorIterator:
    def __init__(self, log_lines):
        self.log_lines = log_lines
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.log_lines):
            line = self.log_lines[self.index]
            self.index += 1
            if "ERROR" in line:
                return line
        raise StopIteration