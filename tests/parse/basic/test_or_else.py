from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Failure, Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        # Stream(abc) --> P{a|b}
        # ==> (a, Stream(bc))
        ("abc", Parser.char("a").or_else(Parser.char("b")), Success("a", "bc")),
        ("abc", Parser.char("a") | Parser.char("b"), Success("a", "bc")),
        # Stream(abc) --> P{b|a}
        # ==> (a, Stream(bc))
        ("abc", Parser.char("b").or_else(Parser.char("a")), Success("a", "bc")),
        ("abc", Parser.char("b") | Parser.char("a"), Success("a", "bc")),
        # Stream(acd) --> P{a|b|c}
        # ==> (a, Stream(bc))
        (
            "acd",
            Parser.char("a").or_else(Parser.char("b")).or_else(Parser.char("c")),
            Success("a", "cd"),
        ),
        (
            "acd",
            Parser.char("a") | Parser.char("b") | Parser.char("c"),
            Success("a", "cd"),
        ),
        # Stream(bcd) --> P{a|b|c}
        # ==> (b, Stream(cd))
        (
            "bcd",
            Parser.char("a").or_else(Parser.char("b")).or_else(Parser.char("c")),
            Success("b", "cd"),
        ),
        (
            "bcd",
            Parser.char("a") | Parser.char("b") | Parser.char("c"),
            Success("b", "cd"),
        ),
        # Stream(bcd) --> P{a|(b|c)}
        # ==> (b, Stream(cd))
        (
            "bcd",
            Parser.char("a").or_else((Parser.char("b")).or_else(Parser.char("c"))),
            Success("b", "cd"),
        ),
        (
            "bcd",
            Parser.char("a") | (Parser.char("b") | Parser.char("c")),
            Success("b", "cd"),
        ),
        # Stream(cde) --> P{a|b|c}
        # ==> (c, Stream(de))
        (
            "cde",
            Parser.char("a").or_else(Parser.char("b")).or_else(Parser.char("c")),
            Success("c", "de"),
        ),
        (
            "cde",
            Parser.char("a") | Parser.char("b") | Parser.char("c"),
            Success("c", "de"),
        ),
        # Stream(b) --> P{a|c}
        # ==> ParseFailure()
        ("b", Parser.char("a").or_else(Parser.char("c")), Failure),
        ("b", Parser.char("a") | Parser.char("c"), Failure),
        # [] --> P{a|b}
        # ==> ParseFailure()
        ("", Parser.char("a").or_else(Parser.char("b")), Failure),
        ("", Parser.char("a") | Parser.char("b"), Failure),
    ],
)
def test_or_else(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
