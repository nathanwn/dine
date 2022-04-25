from dine.stream import Location


def test_location_eq():
    assert Location(1, 1) == Location(1, 1)
    assert Location(1, 1) != (1, 1)


def test_location_str():
    assert str(Location(1, 2)) == "(line=1,col=2)"
    assert str(Location(123, 45)) == "(line=123,col=45)"


def test_location_repr():
    assert repr(Location(1, 2)) == "Location(line=1,col=2)"
    assert repr(Location(123, 45)) == "Location(line=123,col=45)"
