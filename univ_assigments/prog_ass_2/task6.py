import os

folder_name = "data"
os.makedirs(folder_name, exist_ok=True)

for i in range(1, 4):
    with open(f"{folder_name}/file_{i}.txt", "w") as f:
        f.write(f"This is file number {i}")

print("Files in folder:", os.listdir(folder_name))

os.rename("data/file_1.txt", "data/renamed_file.txt")

os.remove("data/file_2.txt")

print("Updated files in folder:", os.listdir(folder_name))