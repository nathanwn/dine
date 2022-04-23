from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        # Stream("a") --> 'a' (COMMA 'a')*
        # ==> Success(["a"], Stream(""))
        (
            "a",
            Parser.string("a").many1_sep_by(Parser.char(",")),
            Success(["a"], ""),
        ),
        # Stream("a,a") --> 'a' (COMMA 'a')*
        # ==> Success(["a", "a"], Stream(""))
        (
            "a,a",
            Parser.string("a").many1_sep_by(Parser.char(",")),
            Success(["a", "a"], ""),
        ),
        # Stream("a,a,a") --> 'a' (COMMA 'a')*
        # ==> Success(["a", "a", "a"], Stream(""))
        (
            "a,a,a",
            Parser.string("a").many1_sep_by(Parser.char(",")),
            Success(["a", "a", "a"], ""),
        ),
        # Stream("a   , a ,  a,  a$") --> 'a' (SPACE* COMMA SPACE* 'a')*
        # ==> Success(["a", "a", "a"], Stream("$"))
        (
            "a   , a ,  a,  a$",
            Parser.char("a").many1_sep_by(
                Parser.sequence(
                    [
                        Parser.char(" ").many0(),
                        Parser.char(","),
                        Parser.char(" ").many0(),
                    ]
                )
            ),
            Success(["a", "a", "a", "a"], "$"),
        ),
    ],
)
def test_many1_sep_by(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
