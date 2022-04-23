from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Failure, Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        # Stream(abcd) --> P{ab}
        # ==> ((a, b), Stream(cd))
        (
            "abcd",
            Parser.char("a").and_then(Parser.char("b")),
            Success(("a", "b"), "cd"),
        ),
        (
            "abcd",
            Parser.char("a") & Parser.char("b"),
            Success(("a", "b"), "cd"),
        ),
        # Stream(abcd) --> P{abc}
        # ==> (((a, b), c), Stream(d))
        (
            "abcd",
            Parser.char("a").and_then(Parser.char("b")).and_then(Parser.char("c")),
            Success((("a", "b"), "c"), "d"),
        ),
        (
            "abcd",
            Parser.char("a") & Parser.char("b") & Parser.char("c"),
            Success((("a", "b"), "c"), "d"),
        ),
        # Stream(abcd) --> P{a(bc)}
        # ==> ((a, (b, c)), Stream(d))
        (
            "abcd",
            Parser.char("a").and_then(Parser.char("b").and_then(Parser.char("c"))),
            Success(("a", ("b", "c")), "d"),
        ),
        (
            "abcd",
            Parser.char("a") & (Parser.char("b") & Parser.char("c")),
            Success(("a", ("b", "c")), "d"),
        ),
        # Stream(abc) --> P{ac}
        # ==> ParseFailure()
        ("abc", Parser.char("a").and_then(Parser.char("c")), Failure),
        ("abc", Parser.char("a") & Parser.char("c"), Failure),
        # Stream(abc) --> P{bc}
        # ==> ParseFailure()
        ("abc", Parser.char("b").and_then(Parser.char("b")), Failure),
        ("abc", Parser.char("b") & Parser.char("b"), Failure),
        # Stream(a) --> P{ab}
        # ==> ParseFailure()
        ("a", Parser.char("a").and_then(Parser.char("b")), Failure),
        ("a", Parser.char("a") & Parser.char("b"), Failure),
        # Stream() --> P{ab}
        # ==> ParseFailure()
        ("", Parser.char("a").and_then(Parser.char("b")), Failure),
        ("", Parser.char("a") & Parser.char("b"), Failure),
    ],
)
def test_and_then(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
