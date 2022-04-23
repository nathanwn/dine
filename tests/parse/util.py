from functools import partial
from typing import TypeVar

from dine.parser import Parser
from dine.result import ParseFailure, ParseResult, ParseSuccess
from dine.stream import Location, Stream

LOC = Location(-1, -1)
Failure = ParseFailure(LOC, "", "")
Success = partial(ParseSuccess, LOC)

A = TypeVar("A")


def helper_success_or_failure(text: str, parser: Parser[A], xresult: ParseResult[A]):
    s = Stream(text)
    result = parser(s)
    match result:
        case ParseSuccess():
            match xresult:
                case ParseSuccess():
                    assert result.val == xresult.val and result.rs == xresult.rs
                case _:
                    assert False
        case _:
            assert isinstance(result, ParseFailure)
