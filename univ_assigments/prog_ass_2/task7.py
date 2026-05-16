import csv
records = [
    ["Alice", 85], ["Bob", 92], ["Charlie", 78], ["Diana", 95], ["Edward", 88]
]

with open("student_grades.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "grade"])
    writer.writerows(records)

grades = []
print("--- Student Records ---")
with open("student_grades.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"Name: {row['name']}, Grade: {row['grade']}")
        grades.append(int(row['grade']))

print(f"\nHighest Grade: {max(grades)}")
print(f"Average Grade: {sum(grades) / len(grades)}")