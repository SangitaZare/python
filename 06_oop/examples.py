"""06 - OOP: classes, encapsulation, inheritance, polymorphism, dunder methods, dataclasses."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

print("=== 1. Class and object ===")


class BankAccount:
    bank_name = "PyBank"  # class attribute, shared by all instances

    def __init__(self, owner, balance=0):
        self.owner = owner      # instance attributes
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def __str__(self):
        return f"{self.owner}: Rs.{self.balance:,.2f}"

    def __repr__(self):
        return f"BankAccount({self.owner!r}, {self.balance})"


acc1 = BankAccount("Sangita", 1000)
acc2 = BankAccount("Ravi")
acc1.deposit(500)
print(acc1, "|", acc2)
print("repr:", [acc1, acc2])
print("shared class attribute:", acc1.bank_name, acc2.bank_name)
print("method call is really:", BankAccount.deposit(acc2, 100))
try:
    acc2.withdraw(9999)
except ValueError as e:
    print("withdraw error:", e)

print("\n=== 2. Encapsulation & @property ===")


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price       # goes through the setter
        self.__secret = "hidden"  # name-mangled

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    @property
    def price_with_tax(self):    # read-only computed property
        return round(self._price * 1.18, 2)


p = Product("Pen", 100)
print("price:", p.price, "| with tax:", p.price_with_tax)
try:
    p.price = -5
except ValueError as e:
    print("setter blocked:", e)
print("__secret mangled to:", [a for a in vars(p) if "secret" in a])

print("\n=== 3. Inheritance & super() ===")


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0, rate=0.04):
        super().__init__(owner, balance)
        self.rate = rate

    def add_interest(self):
        return self.deposit(self.balance * self.rate)

    def withdraw(self, amount):  # override: keep a minimum balance
        if self.balance - amount < 500:
            raise ValueError("Must keep Rs.500 minimum")
        return super().withdraw(amount)


sav = SavingsAccount("Meera", 10000)
sav.add_interest()
print(sav)
try:
    sav.withdraw(10000)
except ValueError as e:
    print("override blocked:", e)
print("isinstance(sav, BankAccount):", isinstance(sav, BankAccount))
print("MRO:", [c.__name__ for c in SavingsAccount.__mro__])

print("\n=== 4. Polymorphism & abstraction ===")


class Shape(ABC):
    @abstractmethod
    def area(self):
        ...

    def describe(self):
        return f"{type(self).__name__} with area {self.area():.2f}"


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return 3.14159 * self.r ** 2


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2


for shape in [Circle(1), Square(2)]:
    print(" ", shape.describe())
try:
    Shape()
except TypeError as e:
    print("abstract class:", e)


class Duck:
    def speak(self):
        return "Quack"


class Robot:
    def speak(self):
        return "Beep"


print("duck typing:", [thing.speak() for thing in (Duck(), Robot())])

print("\n=== 5. Instance / class / static methods ===")


class Date:
    def __init__(self, day, month, year):
        self.day, self.month, self.year = day, month, year

    @classmethod
    def from_string(cls, text):
        d, m, y = map(int, text.split("-"))
        return cls(d, m, y)

    @staticmethod
    def is_valid_month(m):
        return 1 <= m <= 12

    def __repr__(self):
        return f"Date({self.day}, {self.month}, {self.year})"


print("classmethod factory:", Date.from_string("28-10-2026"))
print("staticmethod:", Date.is_valid_month(13))

print("\n=== 6. Dunder methods ===")


class Playlist:
    def __init__(self, name, songs):
        self.name = name
        self.songs = list(songs)

    def __len__(self):
        return len(self.songs)

    def __getitem__(self, i):
        return self.songs[i]

    def __contains__(self, song):
        return song in self.songs

    def __add__(self, other):
        return Playlist(f"{self.name}+{other.name}", self.songs + other.songs)

    def __eq__(self, other):
        return self.songs == other.songs

    def __call__(self):
        return f"Now playing: {self.songs[0]}"

    def __repr__(self):
        return f"Playlist({self.name!r}, {len(self)} songs)"


chill = Playlist("Chill", ["Song A", "Song B"])
party = Playlist("Party", ["Song C"])
print("len:", len(chill), "| [0]:", chill[0], "| in:", "Song B" in chill)
print("add:", chill + party)
print("iterate (via __getitem__):", [s for s in chill])
print("call:", chill())
print("eq:", chill == Playlist("Copy", ["Song A", "Song B"]))

print("\n=== 7. Dataclasses ===")


@dataclass(order=True)
class Student:
    marks: int
    name: str
    subjects: list[str] = field(default_factory=list, compare=False)


students = [Student(88, "Asha"), Student(92, "Ravi", ["Math"]), Student(79, "Meera")]
print(students[0])
print("sorted by marks:", [s.name for s in sorted(students)])
print("equality:", Student(88, "Asha") == Student(88, "Asha"))


@dataclass(frozen=True)
class Point:
    x: int
    y: int


pt = Point(1, 2)
try:
    pt.x = 5
except Exception as e:
    print("frozen:", type(e).__name__)
print("frozen is hashable -> dict key:", {pt: "origin-ish"})

print("\n=== 8. Composition (has-a) ===")


class Engine:
    def start(self):
        return "Engine started"


class Car:
    def __init__(self, model):
        self.model = model
        self.engine = Engine()  # Car HAS an Engine

    def drive(self):
        return f"{self.model}: {self.engine.start()}, driving..."


print(Car("Nexon").drive())

print("\n=== Pitfall: mutable class attribute ===")


class Team:
    members = []  # shared by ALL teams!

    def add(self, name):
        self.members.append(name)


t1, t2 = Team(), Team()
t1.add("Asha")
print("t2.members (never added to):", t2.members)
