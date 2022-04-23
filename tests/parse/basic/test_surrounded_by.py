from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Failure, Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        # Stream("abcdefg") --> TakeBetween(P("ab"), P("cd"), P("ef"))
        # ==> Success("cd", "g")
        (
            "abcdefg",
            Parser.string("cd").surrounded_by(Parser.string("ab"), Parser.string("ef")),
            Success("cd", "g"),
        ),
        (
            "abcdefg",
            Parser.string("cd").surrounded_by(Parser.string("ab"), Parser.string("ef")),
            Success("cd", "g"),
        ),
        # Stream('"abc"') --> TakeBetween(P('"'), P("ab"), P('"'))
        # ==> Success("abc", "")
        (
            '"abc"',
            Parser.string("abc").surrounded_by(Parser.string('"'), Parser.string('"')),
            Success("abc", ""),
        ),
        # Stream('abc"') --> TakeBetween(P('"'), P("abc"), P('"'))
        # ==> ParseFailure()
        (
            'abc"',
            Parser.string("abc").surrounded_by(Parser.string('"'), Parser.string('"')),
            Failure,
        ),
        # Stream('"abc') --> TakeBetween(P('"'), P("abc"), P('"'))
        # ==> ParseFailure()
        (
            '"abc',
            Parser.string("abc").surrounded_by(Parser.string('"'), Parser.string('"')),
            Failure,
        ),
        # Stream('"ab"') --> TakeBetween(P('"'), P("abc"), P('"'))
        # ==> ParseFailure()
        (
            '"ab"',
            Parser.string("abc").surrounded_by(Parser.string('"'), Parser.string('"')),
            Failure,
        ),
    ],
)
def test_surrounded_by(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
