import time
from datetime import datetime

def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__} at {datetime.now()}")
        return func(*args, **kwargs)
    return wrapper

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] {func.__name__} took {end - start:.5f} seconds.")
        return result
    return wrapper