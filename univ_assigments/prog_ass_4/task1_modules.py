import math
import random
import os
from random import choice, shuffle

# 1. math модулі
print("--- Math Module ---")
print(f"Square root of 25: {math.sqrt(25)}")
print(f"Ceiling of 3.1: {math.ceil(3.1)}")
print(f"Value of Pi: {math.pi}")

# 2. random модулі және roll_dice функциясы
print("\n--- Random Module ---")
def roll_dice():
    return random.randint(1, 6)

print("Rolling dice 5 times:", end=" ")
for _ in range(5):
    print(roll_dice(), end=" ")
print()

# 3. os модулі
print("\n--- OS Module ---")
cwd = os.getcwd()
print(f"Current directory: {cwd}")
print(f"Files in directory: {os.listdir(cwd)[:3]}...") # тек алғашқы үшеуін шығару
print(f"Does 'task1_modules.py' exist?: {os.path.exists('task1_modules.py')}")

# 4. from ... import ...
print("\n--- Specific Imports ---")
numbers = [10, 20, 30, 40]
print(f"Choice: {choice(numbers)}")
shuffle(numbers)
print(f"Shuffled list: {numbers}")

# 5. Жеке пакетті шақыру
try:
    from mypackage.utils import greet, is_positive
    print("\n--- My Package ---")
    print(greet("AITU Student"))
    print(f"Is 10 positive?: {is_positive(10)}")
except ImportError:
    print("\n[!] 'mypackage' табылмады. Алдымен папканы жасаңыз.")