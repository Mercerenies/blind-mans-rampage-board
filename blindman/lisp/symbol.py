
class Symbol:
    """Simple type to distinguish Lisp symbols from literal strings.
    The current implementation of the Symbol class is NOT interned and
    is merely a string under the hood.

    """
    _value: str

    def __init__(self, value: str) -> None:
        self._value = value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Symbol):
            return self._value == other._value
        return False

    def __hash__(self) -> int:
        return hash(("Symbol", self._value))

    def __repr__(self) -> str:
        return f"Symbol({self._value!r})"

    def __str__(self) -> str:
        if " " in self._value:
            return f"'|{self._value}|"
        else:
            return f"'{self._value}"
