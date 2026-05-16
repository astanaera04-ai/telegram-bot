import re

print("--- 1. Search Version Number ---")
text1 = 'Welcome to Python 3.11'
match_ver = re.search(r'\d+\.\d+', text1)
if match_ver:
    print(f"Version found: {match_ver.group()}")

print("\n--- 2. Validate Username ---")
# Әріптен басталады, тек әріп/сан/астыңғы сызық, кемі 3 таңба
pattern_user = r'^[a-zA-Z]\w{2,}$'
users = ["a_1", "123user", "valid_user"]
for u in users:
    print(f"User '{u}' -> {bool(re.match(pattern_user, u))}")

print("\n--- 3. Extract Emails ---")
text2 = "Contact us at support@aitu.edu.kz or admin@python.org for help."
emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text2)
print(f"Emails: {emails}")

print("\n--- 4. Censor Phone Numbers ---")
text3 = "Call 701-234-5678 or 727-987-6543 for support."
censored = re.sub(r'\d', '*', text3)
print(censored)

print("\n--- 5. Validate Password ---")
def validate_password(pw):
    # Кемі 8 таңба, 1 бас әріп, 1 сан, 1 арнайы таңба
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%]).{8,}$'
    return bool(re.search(pattern, pw))

print(f"Password 'Weak' -> {validate_password('Weak')}")
print(f"Password 'StrongPass1!' -> {validate_password('StrongPass1!')}")