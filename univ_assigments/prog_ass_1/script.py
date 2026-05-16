name = input("what is your name?")
age = int(input("how old are you?"))
print("Hello", name + ", you will be", age + 1, "next year!\n" )
print("Type of age variable:", type(age))

radius = 42
pi = 3.1415926
s = pi * pow(radius , 2)
print("Area of circle: ",round(s, 4))

point = (23, 34)
dist = (point[0]**2 + point[1]**2) ** 0.5
print(dist <= radius)

a = int(input("Enter a number between 1 and 100: "))
if 1 <= a <= 33:
    print("Small")
elif 34 <= a <= 66:
    print("Medium")
elif 67 <= a <= 100:
    print("Large")
else:
    print("Number out of range")

if a > 10 and a % 2 == 0:
    print("The number is greater than 10 and even")

for i in range(2, 21, 2):
    print(i)

secret = 7
guess = int(input("Guess the number: "))
while guess != secret:
    if guess > secret:
        print("Too high")
    else:
        print("Too low")
    guess = int(input("Try again: "))

print("Correct!")
