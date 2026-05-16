user_note = input("Enter your note: ")

with open("my_notes.txt", "a") as file:
    file.write(user_note + "\n")

print("\n--- Saved Notes ---")
with open("my_notes.txt", "r") as file:
    print(file.read())