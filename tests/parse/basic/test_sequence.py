from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Failure, Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        # Stream(abc) --> P{ab}
        # ==> ([a, b], Stream(c))
        (
            "abcd",
            Parser.sequence([Parser.char("a"), Parser.char("b")]),
            Success(["a", "b"], "cd"),
        ),
        # Stream(abcd) --> P{abc}
        # ==> ([a, b, c], Stream(d))
        (
            "abcd",
            Parser.sequence(
                [
                    Parser.char("a"),
                    Parser.char("b"),
                    Parser.char("c"),
                ]
            ),
            Success(["a", "b", "c"], "d"),
        ),
        # Stream(abcd) --> P{ac}
        # ==> ParseFailure()
        (
            "abcd",
            Parser.sequence([Parser.char("a"), Parser.char("c")]),
            Failure,
        ),
        # Stream(abcd) --> P{cb}
        # ==> ParseFailure()
        (
            "abcd",
            Parser.sequence([Parser.char("c"), Parser.char("b")]),
            Failure,
        ),
        # Stream(a) --> P{ab}
        # ==> ParseFailure()
        (
            "a",
            Parser.sequence([Parser.char("a"), Parser.char("b")]),
            Failure,
        ),
    ],
)
def test_sequence(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
