# ============================================
# Lab 8: Built-in Collections Overview
# ============================================
# Goal: meet the 4 core containers.
#
#   list  -> ordered, changeable, allows duplicates      [ ]
#   tuple -> ordered, FIXED (immutable)                  ( )
#   set   -> unordered, no duplicates                    { }
#   dict  -> key -> value pairs                          {k: v}
#
# Priority for AI/.NET integration work:
#   dict = 60% of what you'll touch (every JSON payload is one)
#   list = 30% (every model output is a list of dicts)
#   tuple unpacking = 9% (ML functions return tuples constantly)
#   set = 1% (skip for now; rediscover when you need to dedupe)


# --------------------------------------------
# LIST: ordered, mutable sequence
# C#: List<string>
# --------------------------------------------
fruits: list[str] = ["apple", "banana", "mango"]

fruits.append("orange")        # add to the end        (C#: fruits.Add("orange"))
fruits[0] = "avocado"          # change by index       (same as C#)

print("list:", fruits, "| length:", len(fruits))   # len() is a built-in, not .Count
print("first:", fruits[0], "| last:", fruits[-1])  # -1 = last element (C#: fruits[^1])

# SLICING — [start:stop], stop is EXCLUSIVE, returns a NEW LIST
# fruits[1:2] -> ["banana"]  (a list with one item, NOT the string "banana")
# C# analogue: fruits.Skip(1).Take(1).ToList()  or  fruits[1..2]
# You will use this constantly in ML code: text[:512] to truncate to max tokens
print("slice [1:2]:", fruits[1:2])


# --------------------------------------------
# TUPLE: like a list but cannot be changed
# C#: (int, int) value tuple
# --------------------------------------------
point = (10, 20)               # good for fixed groups of data

# UNPACKING — the most important pattern in this lab for real ML work.
# Hugging Face / tokenizer functions return tuples; you unpack on arrival:
#   (inputIds, attentionMask, _) = tokenizer.Encode(...)   <- Step 5 of the exercise
# Use _ for values you don't care about (works in C# too).
x, y = point
print("tuple:", point, "| x:", x, "| y:", y)

# point[0] = 99                # TypeError — tuples are immutable


# --------------------------------------------
# SET: unique items, no order
# C#: HashSet<int>
# --------------------------------------------
numbers = {1, 2, 2, 3, 3, 3}   # duplicates are dropped automatically
numbers.add(4)

print("set:", numbers)         # {1, 2, 3, 4}
print("is 2 in set?", 2 in numbers)    # True  ('in' = C#'s .Contains())
# BUG CAUGHT in the original: label said 2 but code checked `20 in numbers`.
# Python ran it happily and printed False — no compiler to save you.
# Lesson: when output surprises you, suspect the print statement first.


# --------------------------------------------
# DICT: key/value lookup table
# C#: Dictionary<string, object> — but the better mental model:
# A DICT IS A LIVE JSON OBJECT. {"name": "Alice"} on the wire
# and in memory look identical. FastAPI request bodies, model
# outputs, config files — all dicts.
# --------------------------------------------
person = {"name": "Alice", "age": 30}

print("dict:", person)
print("name:", person["name"])         # access by key — KeyError if missing!
person["city"] = "Pune"                # add a new key (adding a property at runtime)
person["age"] = 31                     # update a value

print("keys:", list(person.keys()))
print("values:", list(person.values()))

# THE SAFE-ACCESS RULE — memorize this pair:
print(person.get("salary"))            # None  — safe, like TryGetValue
# print(person["salary"])              # KeyError — crashes the program
# In a FastAPI endpoint, .get() = clean error handling; [] = a 500 in production.
# Real-world shape from the exercise:
#   result = clf(req.text)[0]      # index into a LIST -> get a DICT
#   result["label"]                # dict access — you've now done both


# --------------------------------------------
# Choosing the right one
# --------------------------------------------
# Need order + changes?            -> list
# Need fixed, unchangeable data?   -> tuple
# Need uniqueness / fast 'in'?     -> set
# Need to look things up by key?   -> dict  (think: JSON object)


# --------------------------------------------
# Quick conversions — just call the type like a function
# --------------------------------------------
print(list((1, 2, 3)))                 # tuple -> list
print(set([1, 1, 2, 3]))               # list  -> set (removes dups)
print(tuple([1, 2, 3]))                # list  -> tuple
print(set((1, 2, 3, 6, 7, 7, 1, 8)))   # tuple -> set  -> {1, 2, 3, 6, 7, 8}


# --------------------------------------------
# TRY THIS — sorting & aggregates (LINQ's OrderBy / Sum / Max / Min)
# --------------------------------------------
nums = [5, 3, 8, 1]

nums.sort()                            # in-place, mutates nums   (returns None!)
print(nums)                            # [1, 3, 5, 8]

print(sorted(nums, reverse=True))      # returns a NEW list, original untouched
# .sort() vs sorted() = List.Sort() vs items.OrderBy().ToList()
# Classic beginner bug: x = nums.sort() -> x is None, not the sorted list.

print(sum(nums), max(nums), min(nums)) # built-ins, no namespace needed
