import math


def task1():
    def greet(name):
        print(f"Hello, {name}! Welcome to Python.")

    def calculate_area(length, width):
        return length * width

    def is_even(number):
        return number % 2 == 0

    greet("Ali")
    greet("Aisha")
    print("Area (5x10):", calculate_area(5, 10))
    print("Area (7x3):", calculate_area(7, 3))
    print("Is 4 even?", is_even(4))

    
    print("Is 7 even?", is_even(7))


def task2():
    def introduce(name, age=18):
        print(f"My name is {name} and I am {age} years old.")

    def sum_all(*args):
        return sum(args)

    def print_info(**kwargs):
        for key, value in kwargs.items():
            print(f"{key}: {value}")

    introduce("Dias")
    introduce("Madina", 20)
    print("Sum (1, 2, 3, 4, 5):", sum_all(1, 2, 3, 4, 5))
    print("Sum (10, 20):", sum_all(10, 20))
    print_info(name="Arman", major="IT", gpa=3.8)


def task3():
    square = lambda x: x ** 2
    print("Square of 4:", square(4))
    print("Square of 7:", square(7))

    scores = [45, 78, 92, 60, 55, 88, 71, 39]
    boosted_scores = list(map(lambda x: round(x * 1.1), scores))
    print("Boosted Scores:", boosted_scores)

    passing_scores = list(filter(lambda x: x >= 60, scores))
    print("Passing Scores:", passing_scores)

    students_list = [("Ali", 85), ("Sara", 92), ("Erlan", 78)]
    sorted_students = sorted(students_list, key=lambda x: x[1], reverse=True)
    print("Sorted Students:", sorted_students)


def task4():
    class StudentBasic:
        def __init__(self, name, age, gpa):
            self.name = name
            self.age = age
            self.gpa = gpa

        def introduce(self):
            print(f"Hi, I'm {self.name}. I am {self.age} years old.")

        def is_honor_student(self):
            return self.gpa >= 3.5

    s1 = StudentBasic("Aruzhan", 19, 3.8)
    s2 = StudentBasic("Berik", 20, 3.2)
    s3 = StudentBasic("Zhanar", 18, 3.9)

    for s in [s1, s2, s3]:
        s.introduce()
        print("Honor Student?", s.is_honor_student())


def task5():
    class BankAccount:
        def __init__(self, owner, balance=0):
            self.owner = owner
            self.balance = balance

        def deposit(self, amount):
            self.balance += amount
            print(f"Deposited {amount}. New balance: {self.balance}")

        def withdraw(self, amount):
            if amount > self.balance:
                print("Error: Insufficient funds!")
            else:
                self.balance -= amount
                print(f"Withdrew {amount}. New balance: {self.balance}")

        def get_balance(self):
            return self.balance

        def __str__(self):
            return f"Account Owner: {self.owner}, Balance: ${self.balance}"

        def transfer(self,amount,transfer_to):
            self.withdraw(amount)
            transfer_to.deposit(amount)



    acc1 = BankAccount("Daniyar", 100)
    acc2 = BankAccount("Madina")




    print(acc1)
    acc1.deposit(50)
    acc1.withdraw(200)
    acc1.withdraw(100)
    print(acc2)
    acc2.deposit(500)

    acc1.transfer(100,acc2)


def task6():
    class Animal:
        def __init__(self, name, sound):
            self.name = name
            self.sound = sound

        def speak(self):
            print(f"{self.name} says {self.sound}")

    class Dog(Animal):
        def __init__(self, name):
            super().__init__(name, "Woof!")

        def fetch(self):
            print(f"{self.name} fetches the ball!")

    class Cat(Animal):
        def purr(self):
            print(f"{self.name} purrs softly...")

    dog = Dog("Rex")
    cat = Cat("Barsik", "Meow!")
    dog.speak()
    dog.fetch()
    cat.speak()
    cat.purr()


def task7():
    class Book:
        def __init__(self, title, author):
            self.title = title
            self.author = author

    class Library:
        def __init__(self):
            self.books = []

        def add_book(self, book):
            self.books.append(book)

        def remove_book(self, title):
            for book in self.books:
                if book.title == title:
                    self.books.remove(book)
                    return

        def list_books(self):
            for book in self.books:
                print(f"- '{book.title}' by {book.author}")

        def search_book(self, title):
            for book in self.books:
                if book.title == title:
                    print(f"Found: '{book.title}' by {book.author}")
                    return book
            print("Book not found.")

    lib = Library()
    b1 = Book("1984", "George Orwell")
    b2 = Book("The Great Gatsby", "F. Scott Fitzgerald")
    lib.add_book(b1)
    lib.add_book(b2)
    lib.list_books()
    lib.remove_book("1984")
    lib.search_book("The Great Gatsby")


def task8():
    class Shape:
        def area(self):
            return 0

    class Circle(Shape):
        def __init__(self, radius):
            self.radius = radius

        def area(self):
            return math.pi * (self.radius ** 2)

        def __str__(self):
            return f"Circle with radius {self.radius}"

    class Rectangle(Shape):
        def __init__(self, width, height):
            self.width = width
            self.height = height

        def area(self):
            return self.width * self.height

        def __str__(self):
            return f"Rectangle ({self.width}x{self.height})"

    class Triangle(Shape):
        def __init__(self, base, height):
            self.base = base
            self.height = height

        def area(self):
            return 0.5 * self.base * self.height

        def __str__(self):
            return f"Triangle (base: {self.base}, height: {self.height})"

    shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]
    for shape in shapes:
        print(f"{shape} -> Area: {shape.area():.2f}")


def task9():
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    class Student(Person):
        def __init__(self, name, age):
            super().__init__(name, age)
            self.grades = []

        def add_grade(self, grade):
            self.grades.append(grade)

        def average_grade(self):
            if len(self.grades) == 0:
                return 0
            return sum(self.grades) / len(self.grades)

        def is_passing(self):
            return self.average_grade() >= 60

    class Classroom:
        def __init__(self):
            self.students = []

        def add_student(self, student):
            self.students.append(student)

        def list_students(self):
            for s in self.students:
                print(f"{s.name} - Average: {s.average_grade():.1f} - Passing: {s.is_passing()}")

        def top_student(self):
            if not self.students:
                return None
            sorted_students = sorted(self.students, key=lambda s: s.average_grade(), reverse=True)
            return sorted_students[0]

    room = Classroom()

    st1 = Student("Almas", 20)
    st1.add_grade(90)
    st1.add_grade(80)

    st2 = Student("Bota", 19)
    st2.add_grade(50)
    st2.add_grade(60)

    st3 = Student("Miras", 21)
    st3.add_grade(100)
    st3.add_grade(95)

    room.add_student(st1)
    room.add_student(st2)
    room.add_student(st3)

    room.list_students()

    top = room.top_student()
    print(f"Top Student is {top.name} with an average of {top.average_grade():.1f}")



tandau = int(input())

if tandau == 1:
    task1()
elif tandau == 2:
    task2()
elif tandau == 3:
    task3()
elif tandau == 4:
    task4()
elif tandau == 5:
    task5()
elif tandau == 6:
    task6()
elif tandau == 7:
    task7()
elif tandau == 8:
    task8()
elif tandau == 9:
    task9()