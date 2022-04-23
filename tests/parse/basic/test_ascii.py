from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Failure, Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        ("a", Parser.ascii(), Success("a", "")),
        ("abc", Parser.ascii(), Success("a", "bc")),
        ("1a", Parser.ascii(), Failure),
        ("abc", Parser.ascii_lowercase(), Success("a", "bc")),
        ("abc", Parser.ascii_uppercase(), Failure),
        ("ABC", Parser.ascii_uppercase(), Success("A", "BC")),
        ("ABC", Parser.ascii_lowercase(), Failure),
        ("", Parser.ascii_lowercase(), Failure),
    ],
)
def test_ascii(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
