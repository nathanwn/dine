from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        # Stream(abc) --> P(a?)
        # ==> Success(a, Stream(bc))
        (
            "abc",
            Parser.char("a").optional(),
            Success(["a"], "bc"),
        ),
        # Stream(abc) --> P(z?)
        # ==> Success(None, Stream(abc))
        (
            "abc",
            Parser.char("z").optional(),
            Success([], "abc"),
        ),
    ],
)
def test_optional(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
