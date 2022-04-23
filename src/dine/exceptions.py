class ParseException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class InvalidBranchException(ParseException):
    def __init__(self):
        super().__init__("invalid branch")
