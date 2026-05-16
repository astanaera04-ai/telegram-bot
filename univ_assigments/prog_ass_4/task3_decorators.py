# 1. Logger Decorator
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}...")
        result = func(*args, **kwargs)
        print("Done.")
        return result

    return wrapper


@logger
def add(a, b):
    return a + b


@logger
def subtract(a, b):
    return a - b


# 2. Repeat Decorator
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)

        return wrapper

    return decorator


@repeat(3)
def say_hello():
    print("Hello!")


# 3. Require Positive Decorator
def require_positive(func):
    def wrapper(*args, **kwargs):
        if any(arg <= 0 for arg in args):
            print("Error: All arguments must be positive numbers.")
            return
        return func(*args, **kwargs)

    return wrapper


@require_positive
def area(length, width):
    return length * width


# 4. Stacking Decorators
@logger
@repeat(2)
def greet_user(name):
    print(f"Welcome, {name}!")


# Түсіндірме (Comment):
# Декораторлар төменнен жоғары (функцияға жақыннан бастап) қолданылады, ал орындалуы сырттан ішке қарай жүреді.
# Бірінші @logger жұмыс істеп "Calling..." шығарады, сосын @repeat функцияны 2 рет шақырады, соңында @logger "Done." шығарады.

if __name__ == "__main__":
    print("--- Logger ---")
    print(add(5, 5))

    print("\n--- Repeat ---")
    say_hello()

    print("\n--- Require Positive ---")
    print(area(4, 5))
    area(-2, 5)  # Бұл қате туралы хабарлама шығарады

    print("\n--- Stacked Decorators ---")
    greet_user("Almas")