
from .symbol import Symbol

from typing import Any


def parse(input_str: str) -> Any:
    parser = _LispParser(input_str)
    result = parser.parse_sexpr()
    parser.skip_whitespace()
    if not parser.is_eof():
        raise LispParseError("Expected end of input", parser.pos)
    return result


def parse_many(input_str: str) -> list[Any]:
    parser = _LispParser(input_str)
    result = parser.parse_list_contents()
    parser.skip_whitespace()
    if not parser.is_eof():
        raise LispParseError("Expected end of input", parser.pos)
    return result


class _LispParser:

    def __init__(self, input_str: str) -> None:
        self._input_str = input_str
        self.pos = 0

    def is_eof(self) -> bool:
        return self.pos >= len(self._input_str)

    def peek(self) -> str:
        try:
            return self._input_str[self.pos]
        except IndexError:
            raise LispParseError("Unexpected end of input", self.pos)

    def pop(self) -> str:
        value = self.peek()
        self.pos += 1
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
                next_char = self.pop()
                match next_char:
                    case 'n':
                        chars.append('\n')
                    case _:
                        chars.append(next_char)
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
        while self.pos < len(self._input_str) and self.peek() in " \t\n;":
            if self.peek() == ';':
                self._skip_line_comment()
            else:
                self.pos += 1

    def _skip_line_comment(self) -> None:
        self.pop()  # Consume semicolon
        while self.pos < len(self._input_str) and self.peek() != '\n':
            self.pos += 1
        if self.pos < len(self._input_str):
            self.pop()  # Consume newline


class LispParseError(Exception):

    def __init__(self, msg: str, position: int) -> None:
        super().__init__(msg)
        self.position = position

    def __str__(self) -> str:
        return f"At position {self.position}: {self.args[0]}"
