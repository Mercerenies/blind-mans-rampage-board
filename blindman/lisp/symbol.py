
"""Defines the Symbol class, which is a thin wrapper around a string
and is not equal to its corresponding string."""


class Symbol:
    """Simple type to distinguish Lisp symbols from literal strings.
    The current implementation of the Symbol class is NOT interned and
    is merely a string under the hood.

    Under this implementation, a symbol is a string-like value but is not an instance of str.

    """
    _value: str

    __match_args__ = ("_value",)

    def __init__(self, value: str) -> None:
        self._value = value

    def __eq__(self, other: object) -> bool:
        """Compares for value equality. A symbol is equal to another
        symbol if and only if they are represented by the same string.
        Symbols and strings are never equal."""
        if isinstance(other, Symbol):
            return self._value == other._value
        return False

    def __hash__(self) -> int:
        return hash(("Symbol", self._value))

    def __repr__(self) -> str:
        return f"Symbol({self._value!r})"

    def __str__(self) -> str:
        return self._value
