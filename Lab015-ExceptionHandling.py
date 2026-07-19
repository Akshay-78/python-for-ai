# ============================================
# Lab 5: Exception Handling (try / except)
# CORRECTED & RUNNABLE VERSION
# ============================================
# Handle errors gracefully instead of letting the program crash.


# ---- Basic try / except ----
print("--- Basic try / except ---")
try:
    result = 10 / 0
    print("This line never runs")        # execution jumps to except immediately
    print("Neither does this one")
except ZeroDivisionError:
    print("Cannot divide by zero")


# ---- Catching different errors separately ----
print("\n--- Separate except clauses ---")

def safe_divide(text):
    try:
        num = int(text)            # might raise ValueError
        return 10 / num            # might raise ZeroDivisionError
    except ValueError:
        return "Not a valid number"
    except ZeroDivisionError:
        return "Cannot divide by zero"

print(safe_divide("5"))            # 2.0
print(safe_divide("abc"))          # Not a valid number
print(safe_divide("0"))            # Cannot divide by zero


# ---- Capturing the error object with 'as' ----
print("\n--- Capturing the error object ---")
try:
    int("hello")
except ValueError as e:
    print("Error was:", e)         # see the actual message


# ---- try / except / else / finally ----
#   else    -> runs only if NO exception happened
#   finally -> ALWAYS runs (cleanup), error or not
print("\n--- else / finally ---")

def parse(text):
    try:
        value = int(text)
    except ValueError:
        print("parse failed:", repr(text))
    else:
        print("parsed ok:", value)
    finally:
        print("done trying")

parse("42")        # parsed ok: 42       -> done trying
parse("---")       # parse failed        -> done trying
parse("  42  ")    # surprise: whitespace is fine, parses ok!


# ---- raise: trigger an exception yourself ----
print("\n--- raise ---")

def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age is unrealistic")
    return age

try:
    set_age(-5)
except ValueError as e:
    print("Rejected:", e)

try:
    set_age(200)
except ValueError as e:
    print("Rejected:", e)

print("Accepted:", set_age(30))    # valid, no exception


# ---- Custom exception classes ----
# Subclass Exception to create domain-specific errors.
print("\n--- Custom exceptions ---")

class InsufficientFundsError(Exception):
    pass

class Account:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        # Validate FIRST, mutate SECOND — balance stays safe if we raise.
        if amount > self.balance:
            raise InsufficientFundsError(f"Need {amount}, have {self.balance}")
        self.balance -= amount
        return self.balance

acc = Account(100)
try:
    acc.withdraw(500)
except InsufficientFundsError as e:
    print("Blocked:", e)

print("Balance unchanged:", acc.balance)   # still 100 — raise happened before subtraction
print("Withdraw 40, new balance:", acc.withdraw(40))


# ---- Catching multiple types in one line ----
print("\n--- Multiple types in one clause ---")
try:
    data = {"a": 1}
    print(data["b"])
except (KeyError, IndexError) as e:
    print("Lookup failed:", repr(e))   # repr shows the error TYPE, not just 'b'


# ---- except Exception vs bare except ----
# Bare 'except:' catches EVERYTHING, even Ctrl+C (KeyboardInterrupt)
# and SystemExit — it can make your program impossible to stop cleanly.
# 'except Exception:' is the safer "catch almost everything" form.
print("\n--- except Exception (not bare except) ---")
try:
    mystery = [1, 2, 3][99]
except Exception as e:
    print("Caught safely:", repr(e))


# ============================================
# PRACTICE EXERCISES (write your answers below)
# ============================================
#
# 1. Write safe_get(d, key) that returns d[key], or the string
#    "missing" if the key doesn't exist. Use try/except KeyError.
#
# 2. Write read_int() that keeps asking with input() until the user
#    types a valid integer, then returns it. (Hint: while True + try)
#
# 3. Add a deposit(amount) method to Account that raises ValueError
#    if amount <= 0. Test it with try/except.
#
# 4. Create a custom exception AccountFrozenError. Add a self.frozen
#    flag to Account; withdraw should raise AccountFrozenError when
#    frozen is True. Which except clause should come first if you
#    catch both AccountFrozenError and InsufficientFundsError?
#
# 5. Predict the output BEFORE running:
#        def f():
#            try:
#                return "from try"
#            finally:
#                print("finally runs")
#        print(f())
#    Does finally run even when try returns? Run it and check.
