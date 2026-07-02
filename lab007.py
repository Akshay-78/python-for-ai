# ============================================
# Lab 7: Functions
# ============================================
# Goal: define reusable blocks of logic.
#
# Priority for AI/.NET integration work:
#   keyword arguments = 30%  (Hugging Face APIs are keyword-argument city)
#   multiple returns + unpacking = 30%  (the tokenizer pattern from the exercise)
#   default arguments = 20%  (ML functions have 10 defaults; you override 2)
#   functions-as-values = 15%  (this is what decorators are made of)
#   global keyword = 5%  (recognize it, avoid writing it)


# --------------------------------------------
# Basic function with a docstring
# C#: /// <summary> XML doc comment
# --------------------------------------------
def greet(name: str):
    """Return a greeting for the given name."""   # docstring -> help(greet)
    return f"Hello, {name}!"

print(greet("World"))


# --------------------------------------------
# Default arguments
# C#: int Power(int base, int exponent = 2)
# --------------------------------------------
def power(base, exponent=2):       # exponent defaults to 2
    return base ** exponent        # ** is exponent (C#: Math.Pow)

print(power(6))        # 36 — NOT 25! (original comment was wrong: 6**2 = 36)
print(power(2, 10))    # 1024
# Why this matters: every ML call looks like
#   pipeline("sentiment-analysis", model=..., device=-1, batch_size=8, ...)
# — a signature with 10 defaults where you override the 2 you care about.


# --------------------------------------------
# Keyword arguments (pass by name, any order)
# C#: MakeUser(age: 30, name: "Sagar", city: "Mumbai")
# --------------------------------------------
def make_user(name, city, age):
    return f"{name}, {age}, from {city}"

print(make_user(age=30, name="Sagar", city="Mumbai"))


# --------------------------------------------
# Returning multiple values (packed as a tuple)
# This is EXACTLY the Step 5 tokenizer pattern:
#   (inputIds, attentionMask, _) = tokenizer.Encode(...)
# --------------------------------------------
def min_max(numbers):
    return min(numbers), max(numbers)   # returns a tuple (min, max)

low, high = min_max([3, 1, 4, 1, 5, 9])  # unpack the returned tuple
print("min:", low, "max:", high)


# --------------------------------------------
# Type hints (optional, but great for readability/tools)
# Python does NOT enforce these at runtime — add("3", "67") would
# happily concatenate strings. Hints are for humans, IDEs, and Pydantic.
# --------------------------------------------
def add(a: int, b: int) -> int:
    return a + b

print(add(3, 67))


# --------------------------------------------
# Functions are objects: pass them around
# C#: Func<string, string> — but Python skips the type ceremony
#
# BUG CAUGHT in the original — it "worked" by accident:
#     def apply(fn, value): return value(fn)     <- body swapped
#     apply("hello", shout)                      <- call ALSO swapped
# Two mistakes cancelled out and it printed HELLO anyway.
# C#'s type checker would have caught this instantly. Python didn't.
# Lesson: parameter NAMES are your only documentation — keep them honest.
# --------------------------------------------
def shout(text):
    return text.upper()

def whisper(text):
    return text.lower()

def apply(fn, value):       # fn is the function, value is the data
    return fn(value)        # call the function WITH the value

print(apply(shout, "hello"))    # HELLO
print(apply(whisper, "HELLO"))  # hello


# --------------------------------------------
# Scope: local vs global
# Recognize `global` when you see it; avoid writing it.
# In real code, shared state lives in a class or gets passed in.
# --------------------------------------------
counter = 0                    # global

def increment():
    global counter             # without this, `counter += 1` would create
    counter += 1               # a NEW local variable and crash (UnboundLocalError)

increment()
increment()
print("counter:", counter)     # 2


# --------------------------------------------
# A function with NO return gives back None
# C#: void — except Python's "void" still hands you a value: None.
# Same trap as nums.sort() from Lab 8: x = log("hi") -> x is None.
# --------------------------------------------
def log(msg):
    print("LOG:", msg)
    # no return statement

result = log("saved")
print("returned:", result)     # None

# REMOVED from original — this was C# syntax inside the Python file:
#     void something(){
#         // no line of code
#     }
# Uncommented, it's an instant SyntaxError. Python's void is:
def something():
    pass                       # pass = "empty body on purpose" (like { })


# --------------------------------------------
# Closures: a nested function that REMEMBERS its outer variable
# --------------------------------------------
def multiplier(factor):
    def multiply(x):
        return x * factor      # inner function captures `factor`
    return multiply            # return the FUNCTION itself (no parentheses!)

print(multiplier(5)(7))        # 35 — factor=5, x=7 (original comment said factor=2)

times5 = multiplier(5)         # times5 is now a function with factor baked in
print(times5(10))              # 50


# --------------------------------------------
# The dbConnector idea from the original — REBUILT so it works.
# Your instinct was right: capture the connection details once,
# return a function that uses them. That's dependency injection
# without a DI container, and it's a pattern you'll actually use.
#
# The original had three crashes waiting:
#   1. connect_to_db() called with 0 args but defined with 2
#   2. query(str) recursively called the OUTER function with the
#      built-in `str` type as an argument
#   3. nothing ever returned a result
# --------------------------------------------
def db_connector(db_type, connection_string):
    def run_query(query_str):
        # In real code: open connection using the captured values, execute.
        # Here we simulate to show the closure remembering both outer args.
        return f"[{db_type}] executing '{query_str}' via {connection_string}"
    return run_query

pg_db = db_connector("pg", "host=localhost;db=mydb")
print(pg_db("SELECT * FROM users"))
# pg_db carries db_type and connection_string with it forever —
# the caller never needs to know them. In C# you'd inject IDbConnection;
# in Python you can just close over it.


# --------------------------------------------
# TRY THIS — predict before you run:
# --------------------------------------------
# 1. print(add("3", "67"))          -> what happens? (hint: type hints don't enforce)
# 2. x = multiplier(3)
#    print(x)                       -> what prints? (hint: no parentheses = the object)
# 3. def f(items=[]):               -> Google "Python mutable default argument"
#        items.append(1)            -> the ONE famous default-argument trap;
#        return items               -> never use [] or {} as a default value
