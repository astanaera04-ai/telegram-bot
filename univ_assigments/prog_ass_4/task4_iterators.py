# 1. Countdown Iterator
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


# 2. EvenNumbers Iterator
class EvenNumbers:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        value = self.current
        self.current += 2
        return value


# 3. Fibonacci Iterator
class FibonacciIterator:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.n:
            raise StopIteration
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return value


if __name__ == "__main__":
    print("--- Countdown ---")
    for num in Countdown(3):
        print(num, end=" ")

    print("\n\n--- EvenNumbers ---")
    for num in EvenNumbers(8):
        print(num, end=" ")
    print(f"\nList format: {list(EvenNumbers(8))}")

    print("\n--- Fibonacci ---")
    for num in FibonacciIterator(5):
        print(num, end=" ")

    print("\n\n--- Manual next() ---")
    iter_obj = Countdown(1)
    print(next(iter_obj))  # 1 шығарады
    print(next(iter_obj))  # 0 шығарады
    try:
        print(next(iter_obj))  # StopIteration қатесін береді
    except StopIteration:
        print("StopIteration caught! Iterator is empty.")