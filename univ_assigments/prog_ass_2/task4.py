point_a = (10, 20)
point_b = (100, 250)

print(f"Point A: {point_a}")
print(f"Point B: {point_b}")

try:
    point_a[0] = 50
except TypeError as e:
    print(f"\nError: {e}")