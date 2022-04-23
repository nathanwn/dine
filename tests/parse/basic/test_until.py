from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult
from dine.stream import Stream

from ..util import Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        # Stream("abc.def") -> Parse until "."
        # ==> Success("abc", ".def")
        (
            ("abc.def"),
            Parser.until(label="", predicate=lambda c: c == "."),
            Success("abc", Stream(".def")),
        ),
        # Stream(".def") -> Parse until "."
        # ==> Success("", ".def")
        (
            (".def"),
            Parser.until(label="", predicate=lambda c: c == "."),
            Success("", Stream(".def")),
        ),
    ],
)
def test_until(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
