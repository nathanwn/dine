from dine.result import ParseFailure, ParseSuccess
from dine.stream import Location, Stream


def test_result_neq():
    assert ParseSuccess(Location(1, 1), "abc", Stream("def")) != 42
    assert ParseFailure(Location(1, 1), "", "") != 42
