import pytest

from dine.parser import Parser
from dine.stream import Stream


@pytest.mark.parametrize(
    "text, parser",
    [
        ("", Parser.just("z")),
        ("", Parser.just(42)),
        ("abc", Parser.char("a")),
        ("bac", Parser.char("a")),
        ("1a", Parser.digit()),
        ("a1", Parser.digit()),
    ],
)
def test_call(text: str, parser: Parser):
    assert parser(text) == parser(Stream(text))
