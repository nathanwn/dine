from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Success, helper_success_or_failure

A = TypeVar("A")

ASCII_CODE_SUM_PARSER = (
    Parser.satisfy(lambda _: _.islower())
    .map(ord)
    .apply(
        Parser.satisfy(lambda _: _.islower())
        .map(ord)
        .map(lambda lhs: (lambda rhs: lhs + rhs))
    )
)


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        ("ab", ASCII_CODE_SUM_PARSER, Success(195, "")),
        ("xy", ASCII_CODE_SUM_PARSER, Success(241, "")),
    ],
)
def test_apply(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
