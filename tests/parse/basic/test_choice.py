from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Failure, Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        # Stream(abc) --> P(a|b)
        # ==> Success(a, Stream(bc))
        (
            "abc",
            Parser.choice([Parser.char("a"), Parser.char("b")]),
            Success("a", "bc"),
        ),
        # Stream(abc) --> P(a|b)
        # ==> Success(a, Stream(bc))
        (
            "abc",
            Parser.choice([Parser.char("x"), Parser.char("y"), Parser.char("a")]),
            Success("a", "bc"),
        ),
        # Stream("helloworld") --> P("hallo" | "hello")
        # ==> Success(a, Stream(bc))
        (
            "helloworld",
            Parser.choice([Parser.string("hallo"), Parser.string("hello")]),
            Success("hello", "world"),
        ),
        # Stream("abdca") --> P("aba" | "abc" | "abd")
        # ==> Success(a, Stream(bc))
        (
            "abdca",
            Parser.choice(
                [Parser.string("aba"), Parser.string("abc"), Parser.string("abd")]
            ),
            Success("abd", "ca"),
        ),
        # Stream("abdca") --> P("aba" | "abc" | "abe")
        # ==> ParseFailure()
        (
            "abdca",
            Parser.choice(
                [Parser.string("aba"), Parser.string("abc"), Parser.string("abe")]
            ),
            Failure,
        ),
        # Stream("ab") --> P("aba" | "abc" | "abe")
        # ==> ParseFailure()
        (
            "ab",
            Parser.choice(
                [Parser.string("aba"), Parser.string("abc"), Parser.string("abe")]
            ),
            Failure,
        ),
    ],
)
def test_choice(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
