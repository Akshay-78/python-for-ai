"""Lab 5: Exception Handling (try / except).

What is exception handling?
    When Python hits an error at runtime (bad input, missing key,
    division by zero), it raises an *exception*. Unhandled, that crashes
    the program. ``try/except`` lets you catch the exception and respond
    gracefully — show a friendly message, retry, use a fallback — so one
    bad value doesn't take down the whole program.

Agenda:
    1. Basic try / except
    2. Catching different errors separately
    3. Capturing the error object with ``as``
    4. try / except / else / finally
    5. raise: trigger an exception yourself
    6. Custom exception classes
    7. Catching multiple types in one line

Each section is a self-contained ``demo_*`` function. Uncomment the
calls in :func:`main` as you progress through the lab.
"""

from __future__ import annotations


# ============================================
# 1. BASIC TRY / EXCEPT
# ============================================

def demo_basic_try_except() -> None:
    """Handle an error gracefully instead of letting the program crash."""
    # WHY: without try/except, 10 / 0 crashes the whole program with a
    # traceback. Catching it lets us report the problem and keep running.
    try:
        result = 10 / 0                 # raises ZeroDivisionError
        print(result)                   # never reached — flow jumps to except
    except ZeroDivisionError:
        print("Cannot divide by zero")


# ============================================
# 2. CATCHING DIFFERENT ERRORS SEPARATELY
# ============================================

def safe_divide(text: str) -> float | str:
    """Divide 10 by the number in ``text``, returning a message on failure.

    Args:
        text: User input that should contain an integer.

    Returns:
        The quotient, or a human-readable error message.
    """
    # WHY separate except blocks: each failure needs a DIFFERENT response.
    # Bad text is a user-input problem; zero is a math problem. One generic
    # handler couldn't tell the user what actually went wrong.
    try:
        num = int(text)                 # might raise ValueError
        return 10 / num                 # might raise ZeroDivisionError
    except ValueError:
        return "Not a valid number"
    except ZeroDivisionError:
        return "Cannot divide by zero"


def demo_catching_separately() -> None:
    """One try, several except blocks — first matching type wins."""
    print(safe_divide("5"))             # 2.0
    print(safe_divide("abc"))           # Not a valid number
    print(safe_divide("0"))             # Cannot divide by zero


# ============================================
# 3. CAPTURING THE ERROR OBJECT WITH 'as'
# ============================================

def demo_error_object() -> None:
    """Use ``as e`` to inspect the actual error message."""
    # WHY: the exception object carries details (what value failed, why).
    # Capturing it lets you log or display the real cause instead of a
    # vague "something went wrong".
    try:
        int("hello")
    except ValueError as e:
        print("Error was:", e)          # see the actual message


# ============================================
# 4. TRY / EXCEPT / ELSE / FINALLY
# ============================================

def parse(text: str) -> None:
    """Show all four clauses of a try statement in action.

    else    -> runs only if NO exception happened
    finally -> ALWAYS runs (cleanup), error or not
    """
    # WHY else: success code goes here so the try block stays minimal —
    # we only want to catch failures from int(), not from our own prints.
    # WHY finally: cleanup (closing files, releasing connections) must
    # happen no matter what, even if an exception occurred.
    try:
        value = int(text)
    except ValueError:
        print("parse failed")
    else:
        print("parsed ok:", value)
    finally:
        print("done trying")


def demo_else_finally() -> None:
    """Run parse() on good and bad input to watch each clause fire."""
    parse("42")
    parse("---")
    parse("oops")


# ============================================
# 5. RAISE: TRIGGER AN EXCEPTION YOURSELF
# ============================================

def set_age(age: int) -> int:
    """Validate an age, raising ValueError for impossible values.

    Args:
        age: The age to validate.

    Returns:
        The age, unchanged, if it is plausible.

    Raises:
        ValueError: If the age is negative or unrealistically large.
    """
    # WHY raise: fail LOUDLY at the source of the bad data. Silently
    # accepting age=-5 would corrupt data and surface as a confusing bug
    # far away from where the mistake actually happened.
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age is unrealistic")
    return age


def demo_raise() -> None:
    """The caller decides how to handle the rejection."""
    try:
        set_age(-5)
    except ValueError as e:
        print("Rejected:", e)


# ============================================
# 6. CUSTOM EXCEPTION CLASSES
# ============================================

class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the account balance."""
    # WHY a custom class: callers can catch THIS business rule
    # specifically, without accidentally swallowing unrelated errors
    # (a bare ValueError could come from anywhere).


class Account:
    """A minimal bank account demonstrating domain-specific errors."""

    def __init__(self, balance: float) -> None:
        self.balance = balance

    def withdraw(self, amount: float) -> float:
        """Withdraw ``amount``, returning the new balance.

        Raises:
            InsufficientFundsError: If ``amount`` exceeds the balance.
        """
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Need {amount}, have {self.balance}"
            )
        self.balance -= amount
        return self.balance


def demo_custom_exception() -> None:
    """Catch a domain-specific error by its own name."""
    acc = Account(100)
    try:
        acc.withdraw(500)
    except InsufficientFundsError as e:
        print("Blocked:", e)


# ============================================
# 7. CATCHING MULTIPLE TYPES IN ONE LINE
# ============================================

def demo_multiple_types() -> None:
    """Group exceptions in a tuple when the response is the same."""
    # WHY a tuple: KeyError (dict) and IndexError (list) are both
    # "lookup failed" here and get identical handling — a tuple avoids
    # writing two duplicate except blocks.
    try:
        data = {"a": 1}
        print(data["b"])                # raises KeyError
    except (KeyError, IndexError) as e:
        print("Lookup failed:", repr(e))


# ---- TRY THIS (explore on your own) ----
# A bare 'except:' catches EVERYTHING — avoid it; it hides real bugs
# (even typos in your own code) and makes Ctrl+C stop working.
# Prefer catching the specific exception you expect.


def main() -> None:
    """Run the lab demos. Uncomment sections as the lecture progresses."""
    # demo_basic_try_except()
    # demo_catching_separately()
    # demo_error_object()
    # demo_else_finally()
    # demo_raise()

    # These two were active in the original file:
    demo_custom_exception()
    demo_multiple_types()


if __name__ == "__main__":
    main()
