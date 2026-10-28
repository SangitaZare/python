"""01 - Python basics: variables, types, operators, truthiness, conversion."""
import math

print("=== 1. Variables & dynamic typing ===")
x = 10
print(x, type(x))
x = "ten"  # same name, now points to a str
print(x, type(x))

print("\n=== 2. Core data types ===")
age = 25            # int
price = 99.5        # float
is_active = True    # bool
name = "Sangita"    # str
nothing = None      # NoneType
for value in (age, price, is_active, name, nothing):
    print(f"{value!r:>10} -> {type(value).__name__}")
print("isinstance(age, int):", isinstance(age, int))

print("\n=== 3. Arithmetic operators ===")
print("7 / 2   =", 7 / 2)     # true division, always float
print("7 // 2  =", 7 // 2)    # floor division
print("-7 // 2 =", -7 // 2)   # floors toward minus infinity
print("7 % 2   =", 7 % 2)     # remainder
print("2 ** 10 =", 2 ** 10)   # power

print("\n=== Float precision ===")
print("0.1 + 0.2        =", 0.1 + 0.2)
print("0.1 + 0.2 == 0.3 ->", 0.1 + 0.2 == 0.3)
print("math.isclose     ->", math.isclose(0.1 + 0.2, 0.3))

print("\n=== 4. == vs is ===")
a = [1, 2, 3]
b = [1, 2, 3]
c = a
print("a == b:", a == b)  # same values
print("a is b:", a is b)  # different objects
print("a is c:", a is c)  # same object

print("\n=== 5. Mutable vs immutable ===")
c.append(4)  # c and a are the same list
print("a after c.append(4):", a)
s = "hi"
old_id = id(s)
s += "!"     # str is immutable, so this makes a new object
print("str changed object?", id(s) != old_id)

print("\n=== 6. Truthy / falsy ===")
for v in (0, 1, "", " ", [], [0], None, {}):
    print(f"{v!r:>6} -> {bool(v)}")

print("\n=== 'or' returns an operand, not always a bool ===")
username = "" or "guest"
print("'' or 'guest' ->", username)

print("\n=== 7. Type conversion ===")
user_input = "42"  # input() always gives a str like this
print("int('42') + 1 =", int(user_input) + 1)
print("float('3.5')  =", float("3.5"))
print("str(100)      =", repr(str(100)))
print("bool('False') =", bool("False"), " <- non-empty string is truthy!")

try:
    "5" + 5
except TypeError as e:
    print("'5' + 5 ->", "TypeError:", e)
