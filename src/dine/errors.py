class ParseError(Exception):
    """Base parser error."""

    def __init__(self, msg):
        super().__init__(msg)


class InternalError(ParseError):
    """Error raised when there is something wrong with the library."""

    def __init__(self):
        super().__init__(
            "Internal error. Please report this to the author of the library."
        )
