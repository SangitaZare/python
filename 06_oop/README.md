# 06 · Object-Oriented Programming (OOP)

Run the examples:

```bash
python 06_oop/examples.py
```

**OOP** groups **data** (attributes) and **behaviour** (methods) together into objects.
A **class** is the blueprint, and an **object** (instance) is something built from that blueprint.

## 1. Class and object

```python
class BankAccount:
    bank_name = "PyBank"                  # class attribute: shared by ALL accounts

    def __init__(self, owner, balance=0): # constructor: runs when an object is created
        self.owner = owner                # instance attributes: unique to each object
        self.balance = balance

    def deposit(self, amount):            # instance method
        self.balance += amount
        return self.balance

acc = BankAccount("Sangita", 1000)        # create an object
acc.deposit(500)                          # call a method
```

- `self` is the object the method is called on. Python passes it automatically: `acc.deposit(500)` is really `BankAccount.deposit(acc, 500)`.
- `__init__` **initialises** the object. It is not really the constructor; `__new__` creates the object, and you rarely need it.

## 2. The 4 pillars of OOP

| Pillar | Meaning | In Python |
|--------|---------|-----------|
| **Encapsulation** | Keep data and methods together and hide the internal details | `_protected`, `__private`, `@property` |
| **Inheritance** | A child class reuses and extends a parent class | `class Savings(BankAccount):` |
| **Polymorphism** | The same method name behaves differently for each class | `shape.area()` for Circle and Square |
| **Abstraction** | Show *what* an object does and hide *how* | `abc.ABC` with `@abstractmethod` |

## 3. Encapsulation and `@property`

Python has no truly private attributes. It relies on **conventions**:

- `self.name`: public
- `self._name`: "internal, please don't touch" (only a convention)
- `self.__name`: **name mangling**. Python renames it to `_ClassName__name`, which makes accidental access harder.

`@property` lets you add validation while keeping simple attribute syntax:

```python
class Product:
    def __init__(self, price):
        self.price = price          # this goes through the setter below

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value
```

## 4. Inheritance and `super()`

```python
class SavingsAccount(BankAccount):          # child class (inherits from BankAccount)
    def __init__(self, owner, balance=0, rate=0.04):
        super().__init__(owner, balance)    # call the parent's __init__
        self.rate = rate

    def add_interest(self):                 # new method
        self.deposit(self.balance * self.rate)
```

- **Method overriding**: a child defines a method with the same name as one in its parent, and the child's version is used.
- `isinstance(obj, Class)` and `issubclass(Child, Parent)` check type relationships.
- **Multiple inheritance**: `class C(A, B)`. Python decides which parent's method to use with the **MRO** (Method Resolution Order). You can see it with `C.__mro__`.

## 5. Polymorphism and abstraction

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...                # every child MUST implement this

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r ** 2

class Square(Shape):
    def __init__(self, s): self.s = s
    def area(self): return self.s ** 2

for shape in [Circle(1), Square(2)]:
    print(shape.area())                # the same call, different behaviour
```

`Shape()` raises a `TypeError`, because you can't create an object from an abstract class.

**Duck typing**: "If it walks like a duck and quacks like a duck, it's a duck." Python cares about whether an object **has the method**, not about its type.

## 6. Instance, class and static methods

| Kind | Decorator | First parameter | Use for |
|------|-----------|-----------------|---------|
| Instance method | none | `self` | Working with one object's data |
| Class method | `@classmethod` | `cls` | Alternative constructors and class-level data |
| Static method | `@staticmethod` | none | Utility functions that belong with the class |

```python
class Date:
    def __init__(self, d, m, y): ...
    @classmethod
    def from_string(cls, s):            # Date.from_string("28-10-2026")
        d, m, y = map(int, s.split("-"))
        return cls(d, m, y)
    @staticmethod
    def is_valid_month(m):
        return 1 <= m <= 12
```

## 7. Dunder (magic) methods

"Dunder" means **d**ouble **under**score. These methods let your objects work with Python's built-in syntax.

| Method | Triggered by |
|--------|--------------|
| `__init__` | `Obj()` |
| `__str__` | `print(obj)`, `str(obj)`: readable output for users |
| `__repr__` | `repr(obj)`, the console, lists: unambiguous output for developers |
| `__len__` | `len(obj)` |
| `__eq__`, `__lt__` | `==`, `<` (and therefore `sorted`) |
| `__add__` | `obj1 + obj2` |
| `__getitem__` | `obj[i]` |
| `__contains__` | `x in obj` |
| `__iter__` | `for x in obj` |
| `__call__` | `obj()` |

## 8. Dataclasses (modern and recommended)

For classes that mostly **hold data**, `@dataclass` writes `__init__`, `__repr__` and `__eq__` for you.

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    marks: int = 0
    subjects: list[str] = field(default_factory=list)   # safe mutable default

s = Student("Asha", 88)
print(s)                 # Student(name='Asha', marks=88, subjects=[])
```

Useful options: `@dataclass(frozen=True)` makes objects immutable and hashable, and `@dataclass(order=True)` adds `<` and `>` comparisons.

## 9. Composition vs inheritance

- **Inheritance** is an "is-a" relationship: a `SavingsAccount` *is a* `BankAccount`.
- **Composition** is a "has-a" relationship: a `Car` *has an* `Engine`, so you store an `Engine` object inside the `Car`.

Prefer composition when the relationship isn't clearly "is-a". It is more flexible and avoids deep class hierarchies.

## Common mistakes

- Forgetting `self` in a method definition, so calling it raises a `TypeError` about arguments.
- Using a mutable class attribute (`items = []` in the class body). It is **shared by every instance**. Create it in `__init__` instead.
- Forgetting `super().__init__()` in a child class, so the parent's attributes are never set.
- Only defining `__str__` without `__repr__`. Lists of objects still show `<__main__.X object at 0x...>`.

---

## Interview questions

**1. What is the difference between a class and an object?**
A class is a blueprint or template. An object is a concrete instance created from it, with its own data.

**2. What is `self`?**
A reference to the current instance. Python passes it automatically as the first argument of instance methods. The name `self` is only a convention.

**3. Is `__init__` a constructor?**
It is an **initialiser**. `__new__` creates the object, and `__init__` sets up its attributes. In everyday conversation people call `__init__` the constructor.

**4. Explain the 4 pillars of OOP.**
Encapsulation bundles data with methods and hides internal details. Inheritance lets a child class reuse its parent's code. Polymorphism means one interface with many implementations. Abstraction exposes only the essential behaviour (abstract base classes).

**5. What is the difference between `_var` and `__var`?**
`_var` is a convention meaning "internal use". `__var` triggers name mangling to `_ClassName__var`, which avoids accidental overrides in subclasses. Neither is truly private.

**6. What is the difference between `@classmethod`, `@staticmethod` and an instance method?**
An instance method receives `self` and works on one object. A class method receives `cls` and is used for factory methods and class-level state. A static method receives nothing automatically; it is a plain function grouped inside the class.

**7. What is the difference between `__str__` and `__repr__`?**
`__str__` is the readable output for end users (`print`). `__repr__` is the unambiguous output for developers, ideally valid code that could recreate the object. If `__str__` is missing, Python falls back to `__repr__`.

**8. What is MRO?**
The Method Resolution Order: the order in which Python searches classes for a method when there is (multiple) inheritance. It uses the C3 linearisation algorithm. You can see it with `ClassName.__mro__`.

**9. What is `super()` used for?**
It calls a method of the parent class (following the MRO). It is most often used to run the parent's `__init__` from a child class.

**10. What is a dataclass and when would you use one?**
A decorator that generates `__init__`, `__repr__`, `__eq__` and more for classes that mainly store data. It means less boilerplate and fewer bugs.

**11. What is duck typing?**
Python checks behaviour, not type. If an object has the method you need, you can use it, whatever its class.

**12. What is the difference between composition and inheritance?**
Inheritance is "is-a" (a child extends its parent). Composition is "has-a" (an object contains other objects). Composition is usually more flexible.

---

## Practice

1. Create a `Rectangle` class with `width` and `height`, `area()` and `perimeter()` methods, and a `__str__`.
2. Add a `@property` to `Rectangle` that raises a `ValueError` for negative sizes.
3. Create an `Employee` class and a `Manager` child class with an extra `team` list. Override a `describe()` method in `Manager`.
4. Add `__eq__` and `__lt__` to `Employee` (compare by salary), then sort a list of employees.
5. Rewrite `Employee` as a `@dataclass` and compare how much code you saved.
6. Create an abstract `Payment` class with a `pay(amount)` abstract method, plus `UPIPayment` and `CardPayment` classes that implement it.
