from typing import Generic, TypeVar

from dine.stream import Location, Stream

A = TypeVar("A")


class ParseResult(Generic[A]):
    """
    Base class for parse result
    """

    def __init__(self, loc: Location):
        self.loc = loc


class ParseSuccess(ParseResult[A]):
    """
    Result of the parser when it parses successfully
    """

    def __init__(self, loc: Location, val: A, rs: Stream | str):
        super().__init__(loc)
        self.val: A = val
        self.rs: Stream
        match rs:
            case str():
                self.rs = Stream(rs)
            case _:
                self.rs = rs

    def __eq__(self, other: object):
        match other:
            case ParseSuccess():
                return (
                    self.loc == other.loc
                    and self.val == other.val
                    and self.rs == other.rs
                )
            case _:
                return False

    def __repr__(self):
        return (
            "ParseSuccess(\n"
            f"    loc={str(self.loc)},\n"
            f"    val={repr(self.val)},\n"
            f"    rs=Stream({str(self.rs)})\n"
            ")"
        )


class ParseFailure(ParseResult):
    """
    Result of the parser when it does not parse successfully
    """

    def __init__(self, loc: Location, label: str, msg: str):
        super().__init__(loc)
        self.label: str = label
        self.msg: str = msg

    def __repr__(self):
        return (
            "ParseFailure(\n"
            f"    loc={str(self.loc)},\n"
            f"    label={repr(self.label)},\n"
            f"    msg={repr(self.msg)}))\n"
            ")"
        )

    def __eq__(self, other: object):
        match other:
            case ParseFailure():
                return (
                    self.loc == other.loc
                    and self.label == other.label
                    and self.msg == other.msg
                )
            case _:
                return False
