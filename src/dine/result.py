from typing import Generic, TypeVar

from dine.stream import Location, Stream

A = TypeVar("A")


class ParseResult(Generic[A]):
    def __init__(self, loc: Location):
        self.loc = loc


class ParseSuccess(ParseResult[A]):
    def __init__(self, loc: Location, val: A, rs: Stream | str):
        super().__init__(loc)
        self.val: A = val
        self.rs: Stream
        match rs:
            case str():
                self.rs = Stream(rs)
            case _:
                self.rs = rs

    def __str__(self):
        return f"({str(self.val)}, {str(self.rs)})"

    def __repr__(self):
        return f"ParseSuccess({str(self.val)}, Stream({str(self.rs)})))"


class ParseFailure(ParseResult):
    def __init__(self, loc: Location, label: str, msg: str):
        super().__init__(loc)
        self.label: str = label
        self.msg: str = msg

    def __str__(self):
        return f"Error while parsing {self.label}: {self.msg} at {self.loc}"
