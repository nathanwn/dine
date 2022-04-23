from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Failure, Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        # Stream("helloworld") --> P("hello")
        # ==> Success(a, Stream(bc))
        ("helloworld", Parser.string("hello"), Success("hello", "world")),
        # Stream("helloworld") --> P("hallo")
        # ==> ParseFailure()
        ("helloworld", Parser.string("hallo"), Failure),
    ],
)
def test_string(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
