from __future__ import annotations

from typing import Optional, Tuple


class Location:
    def __init__(self, line: int, col: int):
        self.line = line
        self.col = col

    def __eq__(self, other: object) -> bool:
        match other:
            case Location():
                return self.line == other.line and self.col == other.col
            case _:
                return False

    def __str__(self):
        return f"(line={self.line},col={self.col})"

    def __repr__(self):
        return f"Location(line={self.line},col={self.col})"


class Stream:
    def __init__(self, buf: str, begin: int = 0) -> None:
        self.buf: str = buf
        self.begin: int = begin
        self.loc: list[Location] = [Location(1, 1)]
        for i in range(1, len(self.buf)):
            if self.buf[i - 1] == "\n":
                line = self.loc[-1].line + 1
                col = 1
            else:
                line = self.loc[-1].line
                col = self.loc[-1].col + 1
            self.loc.append(Location(line, col))

    def remain(self):
        return self.buf[self.begin :]

    def __eq__(self, other: object) -> bool:
        match other:
            case str(s):
                return self.remain() == s
            case Stream():
                if self.buf is other.buf:
                    return self.begin == other.begin
                else:
                    return str(self) == str(other)
            case _:
                return False

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        return f'"{self.remain()}"'

    def head(self) -> tuple[str, Location] | None:
        """
        Next character in the parse stream and its location

        Returns
        -------
        Optional[Tuple[str, Location]]
            next character in the parse stream and its location, or
            `None` if the stream is exhausted
        """
        if self.begin < len(self.buf):
            return (self.buf[self.begin], self.loc[self.begin])
        else:
            return None

    def tail(self) -> Stream:
        """
        The tail of the parse stream

        Returns
        -------
        Stream
            a new stream including the remaining characters after
            the head of the current stream
        """
        return Stream(self.buf, self.begin + 1)
