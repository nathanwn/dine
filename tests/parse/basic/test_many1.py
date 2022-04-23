from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Failure, Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        # Stream("abcabd") --> P("abc"*)
        # ==> Success(["abc"], Stream("abd"))
        ("abcabd", Parser.string("abc").many1(), Success(["abc"], "abd")),
        # Stream("abcabcabd") --> P("abc"*)
        # ==> Success(["abc", "abc"], Stream("abd"))
        (
            "abcabcabd",
            Parser.string("abc").many1(),
            Success(["abc", "abc"], "abd"),
        ),
        # Stream("abcabcabcabd") --> P("abc"*)
        # ==> Success(["abc", "abc", "abc"], Stream("abd"))
        (
            "abcabcabcabd",
            Parser.string("abc").many1(),
            Success(["abc", "abc", "abc"], "abd"),
        ),
        # Stream("abcabdabc") --> P("abc"*)
        # ==> Success(["abc"], Stream("abdabc"))
        (
            "abcabdabc",
            Parser.string("abc").many1(),
            Success(["abc"], "abdabc"),
        ),
        # Stream("abd") --> P("abc"*)
        # ==> ParseFailure()
        (
            "abd",
            Parser.string("abc").many1(),
            Failure,
        ),
    ],
)
def test_many1(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
