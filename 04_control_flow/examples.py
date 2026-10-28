"""04 - Control flow: if/elif/else, loops, break/continue, comprehensions, match."""

print("=== 1. if / elif / else ===")
for marks in (95, 72, 40):
    if marks >= 90:
        grade = "A"
    elif marks >= 60:
        grade = "B"
    else:
        grade = "C"
    print(f"marks {marks} -> grade {grade}")

age = 25
print("chained comparison 18 <= age < 60:", 18 <= age < 60)
status = "adult" if age >= 18 else "minor"
print("ternary:", status)

print("\n=== 2. for loops ===")
print("range(5):        ", list(range(5)))
print("range(2, 10, 2): ", list(range(2, 10, 2)))
print("range(5, 0, -1): ", list(range(5, 0, -1)))
names = ["Asha", "Ravi", "Meera"]
scores = [88, 92, 79]
for i, name in enumerate(names, start=1):
    print(f"  {i}. {name}")
for name, score in zip(names, scores):
    print(f"  {name}: {score}")

print("\n=== 3. while loop ===")
count = 3
while count > 0:
    print("  countdown", count)
    count -= 1
print("  liftoff!")

print("\n=== 4. break / continue / pass / loop-else ===")
for n in range(1, 10):
    if n == 6:
        print("  break at", n)
        break
    if n % 2 == 0:
        continue  # skip even numbers
    print("  odd:", n)

for n in [3, 7, 11]:
    if n % 2 == 0:
        print("  found even")
        break
else:
    print("  loop-else: no even number found (no break happened)")


def is_prime(num):
    if num < 2:
        return False
    for d in range(2, int(num ** 0.5) + 1):
        if num % d == 0:
            break
    else:
        return True
    return False


print("  primes under 30:", [n for n in range(30) if is_prime(n)])

for _ in range(1):
    pass  # placeholder, does nothing

print("\n=== 5. Comprehensions ===")
words = ["data", "python", "ai", "pandas", "numpy"]
print("squares:      ", [x * x for x in range(6)])
print("evens:        ", [x for x in range(10) if x % 2 == 0])
print("even/odd:     ", ["even" if x % 2 == 0 else "odd" for x in range(4)])
print("long words UP:", [w.upper() for w in words if len(w) > 4])
print("set of lens:  ", {len(w) for w in words})
print("dict w->len:  ", {w: len(w) for w in words})
print("nested pairs: ", [(r, c) for r in range(2) for c in range(2)])
print("generator sum:", sum(x * x for x in range(1_000_000)))

print("\n=== 6. match statement ===")


def handle(command):
    match command.split():
        case ["go", direction]:
            return f"Going {direction}"
        case ["quit" | "exit"]:
            return "Bye"
        case ["add", *numbers] if numbers:
            return f"Sum = {sum(int(n) for n in numbers)}"
        case _:
            return "Unknown command"


for cmd in ("go north", "exit", "add 1 2 3", "dance"):
    print(f"  {cmd!r:12} -> {handle(cmd)}")


def http_status(code):
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case c if 500 <= c < 600:
            return "Server Error"
        case _:
            return "Other"


print("  ", [http_status(c) for c in (200, 404, 503, 301)])

print("\n=== 7. Walrus operator := ===")
items = [1, 2, 3, 4, 5]
if (n := len(items)) > 3:
    print(f"  Too many items: {n}")

print("\n=== FizzBuzz 1..15 ===")
out = []
for i in range(1, 16):
    if i % 15 == 0:
        out.append("FizzBuzz")
    elif i % 3 == 0:
        out.append("Fizz")
    elif i % 5 == 0:
        out.append("Buzz")
    else:
        out.append(str(i))
print(" ", " ".join(out))
