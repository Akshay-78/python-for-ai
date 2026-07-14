"""Lab 14: Dunder (Magic) Methods.

What are dunder methods?
    "Dunder" = Double UNDERscore, e.g. ``__init__``, ``__str__``.
    They are special methods that Python itself calls behind the scenes
    when you use built-in syntax — you almost never call them directly:

        a + b           -> a.__add__(b)
        a == b          -> a.__eq__(b)
        len(x)          -> x.__len__()
        print(x)        -> uses x.__str__()
        x[0]            -> x.__getitem__(0)
        "song" in pl    -> pl.__contains__("song")
        Money(50)       -> Money.__init__(...)

    Operators aren't hardcoded to numbers/strings/lists — they're hooks.
    That's how the built-ins work too: ``5 + 3`` calls ``int.__add__``.
    Define the right dunder and YOUR class joins the same system, so
    ``m1 + m2`` beats ``m1.add_to(m2)`` and ``len(playlist)`` beats
    ``playlist.get_song_count()`` — zero new API for users to learn.
    You also get ecosystem features free: define ``__lt__`` and
    ``sorted()`` works; define ``__getitem__`` and for-loops work.

    No actual magic: dunders are ordinary methods with a naming
    convention. ``Money(100).__add__(Money(50))`` works if called
    directly — ``+`` is just the pretty way to say it. Many more exist:
    ``__call__`` (callable objects), ``__enter__``/``__exit__``
    (``with`` blocks), ``__iter__``/``__next__`` (custom iteration).

Agenda:
    1. __str__ vs __repr__          (display)
    2. __add__, __eq__, __lt__      (operators)
    3. Container dunders            (__len__, __getitem__, __contains__)
    4. TRY THIS: __mul__            (exercise)

Each section is a self-contained ``demo_*`` function. Uncomment the
calls in :func:`main` as you progress through the lab.
"""

from __future__ import annotations


class Money:
    """An amount in a currency, with operator support via dunders."""

    def __init__(self, amount: float, currency: str = "INR") -> None:
        self.amount = amount
        self.currency = currency

    # ---- __str__ : what print() / str() shows (human-friendly) ----
    # WHY: without it, print(Money(50)) shows an unhelpful memory
    # address like <__main__.Money object at 0x7f...>.
    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"

    # ---- __repr__ : the "developer" representation (debugging, REPL) ----
    # WHY: containers use repr for their elements — this is what makes
    # printing a LIST of Money readable. Convention: look like the code
    # that would recreate the object.
    def __repr__(self) -> str:
        return f"Money({self.amount!r}, {self.currency!r})"

    # ---- __add__ : enables the + operator ----
    # WHY: 'a + b' reads far better than 'a.add_to(b)', and validating
    # inside __add__ means EVERY addition is currency-checked — callers
    # can't forget.
    def __add__(self, other: Money) -> Money:
        if not isinstance(other, Money):
            return NotImplemented       # let Python raise a clear TypeError
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)

    # ---- __eq__ : enables == comparison ----
    # WHY: by default == compares object IDENTITY (same object in
    # memory), so Money(50) == Money(50) would be False without this.
    # NOTE: defining __eq__ makes instances unhashable (no dict keys /
    # sets) unless you also define __hash__ — fine for this lab.
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented       # don't crash on Money(50) == "50"
        return self.amount == other.amount and self.currency == other.currency

    # ---- __lt__ : enables < (and lets sorted() work) ----
    # WHY: sorted() only needs <. Define one dunder, get sorting free.
    def __lt__(self, other: Money) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount < other.amount


def demo_repr_in_containers() -> None:
    """Printing a list of objects uses each element's __repr__."""
    wallet = [Money(10), Money(20), Money(30)]
    print(wallet)               # [Money(10, 'INR'), Money(20, 'INR'), ...]


def demo_money_operators() -> None:
    """Watch each dunder fire from ordinary syntax."""
    total = Money(100) + Money(50)                  # uses __add__
    print("total:", total)                          # __str__  -> "150 INR"
    print("repr :", repr(total))                    # __repr__ -> Money(150, 'INR')
    print("equal?", Money(50) == Money(50))         # __eq__ -> True
    print("sorted:", sorted([Money(30), Money(10), Money(20)]))    # __lt__


# ============================================
# A CONTAINER-LIKE OBJECT
# ============================================

class Playlist:
    """A song collection that behaves like a built-in container."""

    def __init__(self) -> None:
        self.songs: list[str] = []

    def add(self, song: str) -> None:
        """Append a song to the playlist."""
        self.songs.append(song)

    # WHY container dunders: users already know len(), [], 'in', and
    # for-loops. Supporting that syntax means zero new API to learn.
    def __len__(self) -> int:               # enables len(playlist)
        return len(self.songs)

    def __getitem__(self, index: int) -> str:   # enables playlist[0] AND for-loops
        # WHY for-loops work: Python's fallback iteration protocol calls
        # __getitem__ with 0, 1, 2, ... until IndexError.
        return self.songs[index]

    def __contains__(self, song: str) -> bool:  # enables 'song in playlist'
        return song in self.songs


def demo_playlist() -> None:
    """Built-in syntax on a custom container."""
    pl = Playlist()
    pl.add("Song A")
    pl.add("Song B")

    print("length:", len(pl))               # __len__      -> 2
    print("first :", pl[0])                 # __getitem__  -> "Song A"
    print("has B?", "Song B" in pl)         # __contains__ -> True
    for song in pl:                          # works because of __getitem__
        print("playing:", song)


# ---- TRY THIS (explore on your own) ----
# Add __mul__ to Money so 'Money(50) * 3' works:
#
#     def __mul__(self, factor: float) -> Money:
#         return Money(self.amount * factor, self.currency)
#
# Bonus: also add __rmul__ = __mul__ so '3 * Money(50)' works too.


def main() -> None:
    """Run the lab demos. Uncomment sections as the lecture progresses."""
    demo_repr_in_containers()       # this was active in the original file
    # demo_money_operators()
    # demo_playlist()


if __name__ == "__main__":
    main()
