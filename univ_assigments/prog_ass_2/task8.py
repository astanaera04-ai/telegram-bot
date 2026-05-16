import json

user = {
    "name": "Alex",
    "age": 28,
    "skills": ["Python", "JavaScript"]
}

with open("user_data.json", "w") as f:
    json.dump(user, f, indent=4)

with open("user_data.json", "r") as f:
    loaded_user = json.load(f)

loaded_user["skills"]
with open("user_data.json", "w") as f:
    json.dump(loaded_user, f, indent=4)

print("User skills updated and saved to JSON.")