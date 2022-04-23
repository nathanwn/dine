from dine.stream import Location


def test_location_eq():
    assert Location(1, 1) == Location(1, 1)
    assert Location(1, 1) != (1, 1)
