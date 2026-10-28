"""03 - Collections: list, tuple, set, dict, copying, collections module."""
import copy
from collections import Counter, defaultdict, deque, namedtuple

print("=== 1. List ===")
fruits = ["apple", "banana"]
fruits.append("mango")
fruits.insert(0, "kiwi")
fruits.extend(["fig", "pear"])
print("after adds:  ", fruits)
fruits.remove("banana")
last = fruits.pop()
print("popped:", last, "| now:", fruits)
print("sorted() new list:", sorted(fruits), "| original:", fruits)
result = fruits.sort()
print("sort() returns:", result, "| list now:", fruits)
nums = [10, 20, 30, 40, 50]
print("nums[1:3] =", nums[1:3], "| nums[::-1] =", nums[::-1])

print("\n=== 2. Tuple ===")
point = (10, 20)
x, y = point
print("unpacked:", x, y)
print("type((5))  =", type((5)).__name__)
print("type((5,)) =", type((5,)).__name__)
a, b = 1, 2
a, b = b, a
print("swapped:", a, b)
try:
    point[0] = 99
except TypeError as e:
    print("point[0] = 99 -> TypeError:", e)
locations = {(18.5, 73.8): "Pune"}  # a tuple works as a dict key
print("tuple as key:", locations[(18.5, 73.8)])

print("\n=== 3. Set ===")
tags = {"python", "data", "python"}
print("duplicates removed:", sorted(tags))
tags.add("ml")
tags.discard("java")  # no error
print("type({}) =", type({}).__name__, "| type(set()) =", type(set()).__name__)
s1, s2 = {1, 2, 3}, {2, 3, 4}
print("union", s1 | s2, "| intersection", s1 & s2,
      "| difference", s1 - s2, "| symmetric", s1 ^ s2)
items = [3, 1, 3, 2, 1]
print("dedupe keep order:", list(dict.fromkeys(items)))

print("\n=== 4. Dict ===")
student = {"name": "Sangita", "age": 25}
student["city"] = "Pune"
print(student)
print("get missing:", student.get("email"), "| with default:", student.get("email", "N/A"))
try:
    student["email"]
except KeyError as e:
    print("student['email'] -> KeyError:", e)
student.update({"age": 26, "course": "Python"})
del student["city"]
for key, value in student.items():
    print(f"  {key}: {value}")
print("'name' in student:", "name" in student)
d1, d2 = {"a": 1, "b": 2}, {"b": 99, "c": 3}
print("merge d1 | d2:", d1 | d2)

print("\n=== 5. Copy: assignment vs shallow vs deep ===")
original = [1, 2, 3]
alias = original
alias.append(4)
print("alias changed original:", original)
nested = [[1, 2], [3, 4]]
shallow = nested.copy()
deep = copy.deepcopy(nested)
nested[0].append(99)
print("nested :", nested)
print("shallow:", shallow, "<- inner list is shared")
print("deep   :", deep, "<- fully independent")
trap = [[0]] * 3
trap[0].append(1)
print("[[0]] * 3 trap:", trap, "<- the same inner list 3 times")

print("\n=== 6. Unpacking & built-ins ===")
first, *rest = [1, 2, 3, 4]
print("first:", first, "rest:", rest)
names, scores = ["Asha", "Ravi", "Meera"], [88, 92, 79]
report = dict(zip(names, scores))
print("zip ->", report)
print("topper:", max(report, key=report.get))
for i, n in enumerate(names, start=1):
    print(f"  {i}. {n}")

print("\n=== 7. collections module ===")
print("Counter:", Counter("mississippi").most_common(2))
groups = defaultdict(list)
for word in ["apple", "avocado", "banana", "blueberry", "cherry"]:
    groups[word[0]].append(word)
print("defaultdict:", dict(groups))
Point = namedtuple("Point", "x y")
p = Point(3, 4)
print("namedtuple:", p, "| p.x =", p.x)
dq = deque([1, 2, 3])
dq.appendleft(0)
dq.pop()
print("deque:", list(dq))
