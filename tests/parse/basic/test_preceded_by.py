from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Failure, Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        # Stream("abcdef") --> TakeRight(P("ab"), P("cd"))
        # ==> Success("cd", "ef")
        (
            "abcdef",
            Parser.string("cd").preceded_by(Parser.string("ab")),
            Success("cd", "ef"),
        ),
        # Stream("abefcd") --> TakeLeft(P("ab"), P("cd"))
        # ==> ParseFailure()
        ("abefcd", Parser.string("cd").preceded_by(Parser.string("ab")), Failure),
        # Stream("abcdef") --> TakeLeft(P("az"), P("cd"))
        # ==> ParseFailure()
        ("abcdef", Parser.string("cd").preceded_by(Parser.string("az")), Failure),
    ],
)
def test_preceded_by(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
