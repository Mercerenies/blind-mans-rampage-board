
from .symbol import Symbol

from typing import Any


def parse(input_str: str) -> Any:
    parser = _LispParser(input_str)
    return parser.parse_sexpr()


def parse_many(input_str: str) -> list[Any]:
    parser = _LispParser(input_str)
    return parser.parse_list_contents()


class _LispParser:

    def __init__(self, input_str: str) -> None:
        self._input_str = input_str
        self._pos = 0

    def is_eof(self) -> bool:
        return self._pos >= len(self._input_str)

    def peek(self) -> str:
        try:
            return self._input_str[self._pos]
        except IndexError:
            raise LispParseError("Unexpected end of input")

    def pop(self) -> str:
        value = self.peek()
        self._pos += 1
        return value

    def parse_sexpr(self) -> Any:
        self.skip_whitespace()
        if self.peek() == '(':
            return self.parse_list()
        elif self.peek() == '"':
            return self.parse_string()
        else:
            atom = self.parse_atom()
            try:
                return int(atom)
            except ValueError:
                return Symbol(atom)

    def parse_string(self) -> str:
        self.pop()  # Consume opening quote
        chars = []
        while self.peek() != '"':
            next_char = self.pop()
            if next_char == '\\':
                chars.append(self.pop())
            else:
                chars.append(next_char)
        self.pop()  # Consume closing quote
        return ''.join(chars)

    def parse_atom(self) -> str:
        chars = []
        while (not self.is_eof()) and self.peek() not in " \t\n()":
            chars.append(self.pop())
        return ''.join(chars)

    def parse_list(self) -> list[Any]:
        self.pop()  # Consume opening parenthesis
        lst = self.parse_list_contents()
        self.pop()  # Consume closing parenthesis
        return lst

    def parse_list_contents(self) -> list[Any]:
        lst = []
        while True:
            self.skip_whitespace()
            if self.is_eof() or self.peek() == ')':
                break
            lst.append(self.parse_sexpr())
        return lst

    def skip_whitespace(self) -> None:
        while self._pos < len(self._input_str) and self.peek() in " \t\n":
            self._pos += 1


class LispParseError(Exception):
    pass
