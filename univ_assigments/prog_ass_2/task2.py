users  = set()

while True:
    b = input("input usernames one by one:")
    if b == "exit":
        break
    users.add(b)

print("Print the total number of unique users" , len(users))

s = input()
if s in users:
    print("exist")
else:
    print("do not exist")