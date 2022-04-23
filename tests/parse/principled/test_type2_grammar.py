import pytest

from dine.parser import Parser
from dine.result import ParseResult

from ..util import Failure, Success, helper_success_or_failure


@pytest.mark.parametrize(
    "input_text, xresult",
    [
        ("ab", Success("ab", "")),
        ("abc", Success("ab", "c")),
        ("aabb", Success("aabb", "")),
        ("aabbc", Success("aabb", "c")),
        ("aaabbb", Success("aaabbb", "")),
        ("aaabbbc", Success("aaabbb", "c")),
        ("c", Failure),
        ("aab", Failure),
        ("aaabb", Failure),
    ],
)
def test_type2_grammar(input_text: str, xresult: ParseResult):
    """
    Try to parse the following grammar rule:
        S := 'a' S 'b'
    The following is a way to go about parsing this grammar rule, using `p_ntimes`
    """

    S_parser = (
        Parser.char("a")
        .many1()
        .map("".join)
        .bind(
            lambda a_seq: Parser.char("b")
            .times(len(a_seq))
            .map("".join)
            .map(lambda b_seq: a_seq + b_seq)
        )
    )

    helper_success_or_failure(input_text, S_parser, xresult)
