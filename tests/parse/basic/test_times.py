from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult
from dine.stream import Stream

from ..util import Failure, Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        (
            "aaaa",
            Parser.char("a").times(4).map(lambda ls: "".join(ls)),
            Success("aaaa", Stream("")),
        ),
        (
            "aaaa",
            Parser.char("a").times(4).map(lambda ls: "".join(ls)),
            Success("aaaa", Stream("")),
        ),
        (
            "aaaa",
            Parser.char("a").times(3).map(lambda ls: "".join(ls)),
            Success("aaa", Stream("a")),
        ),
        (
            "aaaa",
            Parser.char("a").times(3).map(lambda ls: "".join(ls)),
            Success("aaa", Stream("a")),
        ),
        ("aaaa", Parser.char("a").times(5).map(lambda ls: "".join(ls)), Failure),
        ("aaaa", Parser.char("a").times(5).map(lambda ls: "".join(ls)), Failure),
        ("baaa", Parser.char("a").times(5).map(lambda ls: "".join(ls)), Failure),
    ],
)
def test_times(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
