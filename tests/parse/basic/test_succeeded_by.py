from typing import TypeVar

import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Failure, Success, helper_success_or_failure

A = TypeVar("A")


@pytest.mark.parametrize(
    "text, parser, xresult",
    [
        # Stream("abcdef") --> TakeLeft(P("ab"), P("cd"))
        # ==> Success("ab", "ef")
        (
            "abcdef",
            Parser.string("ab").succeeded_by(Parser.string("cd")),
            Success("ab", "ef"),
        ),
        # Stream("abefcd") --> TakeLeft(P("ab"), P("cd"))
        # ==> ParseFailure()
        ("abefcd", Parser.string("ab").succeeded_by(Parser.string("cd")), Failure),
        # Stream("abcdef") --> TakeLeft(P("az"), P("cd"))
        # ==> ParseFailure()
        ("abcdef", Parser.string("az").succeeded_by(Parser.string("cd")), Failure),
    ],
)
def test_succeeded_by(
    text: str,
    parser: Parser[A],
    xresult: ParseResult[A],
):
    helper_success_or_failure(text, parser, xresult)
