import sys


# 1. Squares Generator
def squares(n):
    for i in range(1, n + 1):
        yield i ** 2


# 2. Infinite Natural Numbers
def natural_numbers():
    n = 1
    while True:
        yield n
        n += 1


# 3. Read Words Generator
def read_words(text):
    for word in text.split():
        yield word


if __name__ == "__main__":
    print("--- Squares ---")
    for s in squares(5):
        print(s, end=" ")

    print("\n\n--- Infinite Generator ---")
    gen = natural_numbers()
    for _ in range(10):  # Тек алғашқы 10 санды аламыз
        print(next(gen), end=" ")

    print("\n\n--- Read Words ---")
    for w in read_words("Python is very awesome"):
        print(w)

    print("\n--- Memory Comparison ---")
    n = 1_000_000
    list_version = [x ** 2 for x in range(n)]
    gen_version = (x ** 2 for x in range(n))

    print(f"List memory size: {sys.getsizeof(list_version)} bytes")
    print(f"Generator memory size: {sys.getsizeof(gen_version)} bytes")

    # Түсіндірме:
    # Тізім (list) барлық 1,000,000 санды бірден жадқа (RAM) сақтайды, сондықтан көп орын алады.
    # Генератор әр санды тек қажет кезде (yield) жасайды, сондықтан жадты өте аз қажет етеді.