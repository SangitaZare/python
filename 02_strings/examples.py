"""02 - Strings: indexing, slicing, immutability, methods, f-strings."""
from collections import Counter

print("=== 1. Creating strings ===")
multi = """Line one
Line two"""
print(multi)
print("Tab:\tafter tab")
print(r"Raw string keeps C:\new\folder as-is")

print("\n=== 2. Indexing & slicing ===")
s = "Python"
print("s[0]    =", s[0])
print("s[-1]   =", s[-1])
print("s[1:4]  =", s[1:4])
print("s[:3]   =", s[:3])
print("s[3:]   =", s[3:])
print("s[::2]  =", s[::2])
print("s[::-1] =", s[::-1])
print("s[2:100] =", s[2:100], "(slicing out of range is fine)")
try:
    s[100]
except IndexError as e:
    print("s[100] -> IndexError:", e)

print("\n=== 3. Immutability ===")
word = "hello"
try:
    word[0] = "H"
except TypeError as e:
    print("word[0] = 'H' -> TypeError:", e)
word.upper()  # result is thrown away, word is unchanged
print("after word.upper():", word)
word = word.upper()  # save the new string
print("after word = word.upper():", word)

print("\n=== 4. Useful methods ===")
text = "  Hello, Python World  "
print(repr(text.strip()))
print(text.strip().lower())
print("hello world".title())
print("a-b-c".replace("-", "+"))
print("a,b,c".split(","))
print("-".join(["2026", "10", "28"]))
print("hello".find("l"), "hello".find("z"))
print("banana".count("a"))
print("report.py".endswith(".py"))
print("123".isdigit(), "abc".isalpha(), "abc123".isalnum())
print("py" in "python")

print("\n=== split() vs split(' ') ===")
messy = "a  b\tc"
print("split()   ->", messy.split())
print("split(' ') ->", messy.split(" "))

print("\n=== 5. f-strings ===")
name, price, qty = "Pen", 12.5, 1234567
print(f"{name} costs {price}")
print(f"{price:.2f}")
print(f"{qty:,}")
print(f"{0.256:.1%}")
print(f"[{name:>10}]")
print(f"[{name:<10}]")
print(f"[{name:^10}]")
print(f"{name=}")
print(f"Total: {price * 3:.2f}")

print("\n=== 6. Looping ===")
for i, ch in enumerate("abc"):
    print(i, ch)

print("\n=== Interview snippets ===")
phrase = "Never odd or even"
clean = phrase.lower().replace(" ", "")
print(f"Is {phrase!r} a palindrome? {clean == clean[::-1]}")
print("Character counts:", Counter("banana"))

parts = []
for n in range(5):
    parts.append(str(n))
print("join instead of += :", ",".join(parts))

print("'10' > '9' ->", "10" > "9", "(compared alphabetically, not as numbers)")
