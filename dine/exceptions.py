class ParseException(Exception):  # pragma: no cover
    def __init__(self, msg):
        super().__init__(msg)


class InvalidBranchException(ParseException):  # pragma: no cover
    def __init__(self):
        super().__init__("invalid branch")
