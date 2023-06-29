from __future__ import annotations

import string
from collections.abc import Callable, Iterable
from functools import reduce
from itertools import chain
from typing import Generic, ParamSpec, TypeVar

from dine.errors import InternalError
from dine.result import ParseFailure, ParseResult, ParseSuccess
from dine.stream import Location, Stream

# Type Variables
A = TypeVar("A")
B = TypeVar("B")
P = ParamSpec("P")
ParseFunc = Callable[[Stream], ParseResult[A]]


class Parser(Generic[A]):
    """The Parser class."""

    def __init__(self: Parser[A], parse_fn: ParseFunc[A], *, label: str | None):
        self.parse_fn: ParseFunc[A] = parse_fn
        self.label: str = label or str(id(self))

    def __call__(self: Parser[A], s: Stream | str) -> ParseResult[A]:
        match s:
            case str():
                stream = Stream(s)
            case Stream():
                stream = s
            case _:
                raise InternalError()
        result = self.parse_fn(stream)
        match result:
            case ParseSuccess():
                return result
            case ParseFailure(loc=loc, label=label, msg=msg):
                if self.label is not None:
                    label = self.label
                return ParseFailure(loc, label, msg)
            case _:
                raise InternalError()

    def set_label(self: Parser[A], label: str) -> Parser[A]:
        """Set the label of the parser.

        label : str
            The label.

        Returns
        -------
        Parser[A]
            The current parser.
        """
        self.label = label
        return self

    def and_then(self: Parser[A], other: Parser[B]) -> Parser[tuple[A, B]]:
        """Parses A and then B.

        Parameters
        ----------
        other : Parser[B]
            B parser

        Returns
        -------
        Parser[Tuple[A, B]]
        """

        def parse(s: Stream) -> ParseResult[tuple[A, B]]:
            result_a: ParseResult[A] = self(s)
            match result_a:
                case ParseFailure():
                    return result_a
                case ParseSuccess(loc=loc_a, val=a, rs=rs_a):
                    result_b: ParseResult[B] = other(rs_a)
                    match result_b:
                        case ParseFailure():
                            return result_b
                        case ParseSuccess(loc=_, val=b, rs=rs_b):
                            return ParseSuccess(loc=loc_a, val=(a, b), rs=rs_b)
            raise InternalError()

        label = f"{self.label} and then {other.label}"
        return Parser(parse, label=label)

    def __and__(self: Parser[A], other: Parser[B]) -> Parser[tuple[A, B]]:
        return self.and_then(other)

    def or_else(self: Parser[A], other: Parser[B]) -> Parser[A | B]:
        """Create a parser that parses ``A`` or ``B``.

        Parameters
        ----------
        other : Parser[B]
            Parser for ``B``.

        Returns
        -------
        Parser[Union[A, B]]
        """

        def parse_fn(s: Stream) -> ParseResult[A | B]:
            res_a = self(s)
            match res_a:
                case ParseSuccess(loc=loc_a, val=a, rs=rs_a):
                    return ParseSuccess(loc_a, a, rs_a)
                case ParseFailure():
                    res_b = other(s)
                    match res_b:
                        case ParseSuccess(loc=loc_b, val=b, rs=rs_b):
                            return ParseSuccess(loc_b, b, rs_b)
                        case ParseFailure():
                            return res_b
            raise InternalError()

        label = f"{self.label} or else {other.label}"
        return Parser(parse_fn, label=label)

    def __or__(self: Parser[A], other: Parser[B]) -> Parser[A | B]:
        """Create a parser that parses ``A`` or ``B``.

        Parameters
        ----------
        other : Parser[B]
            Parser for ``B``.

        Returns
        -------
        Parser[Union[A, B]]
        """
        return self.or_else(other)  # type: ignore

    def map(self: Parser[A], f: Callable[[A], B]) -> Parser[B]:
        """
        If the parser parses successfully, pass the result to a function

        Parameters
        ----------
        f : Callable[[A], B]
            the function that takes the output of the parser and convert it to a new
            object

        Returns
        -------
        Parser[B]
        """

        def parse_fn(s: Stream) -> ParseResult[B]:
            result: ParseResult[A] = self(s)
            match result:
                case ParseSuccess(loc=loc, val=val, rs=rs):
                    return ParseSuccess(loc, f(val), rs)
                case ParseFailure():
                    return result
            raise InternalError()

        return Parser(parse_fn, label=self.label)

    def bind(self: Parser[A], f: Callable[[A], Parser[B]]) -> Parser[B]:
        """
        This method may be used to put a parser after the current parser, with the
        later parser potentially depends on the output of the current parser.

        This method passes the output of the current parser to the function `f`
        to create a new parser. This new parser will take the remaining of the parse
        stream if the current parser parses successfully. This method is akin to the
        bind function in functional programming.

        Parameters
        ----------
        f : Callable[[A], Parser[B]]
            A parser creating function that takes an object of type A (the type of
            the current parser) and create a parser of type B. If the current parser
            successfully parses, the B parser then takes the remaining stream
            from the result of the current parser.

        Returns
        -------
        Parser[B]
            A parser for ``B``.
        """

        label = ""

        def parse_fn(s: Stream) -> ParseResult[B]:
            nonlocal label
            result_a = self(s)

            match result_a:
                case ParseFailure(label=label_a):
                    label = label_a
                    return result_a
                case ParseSuccess(loc=loc_a, val=a, rs=rs_a):
                    parser_b: Parser[B] = f(a)
                    result_b = parser_b(rs_a)
                    match result_b:
                        case ParseFailure(label=label_b):
                            label = label_b
                            return result_b
                        case ParseSuccess(loc=_, val=b, rs=rs_b):
                            return ParseSuccess(loc_a, b, rs_b)
                        case _:  # pragma: no cover
                            raise InternalError()
                case _:  # pragma: no cover
                    raise InternalError()

        return Parser(parse_fn, label=label)

    def apply(self: Parser[A], f_parser: Parser[Callable[[A], B]]) -> Parser[B]:
        """
        Functional apply function for parsers.

        This function takes a parser that parses a converting function from type `A`
        to type `B` and converts it into a function that converts a parser of `A`
        to a parser of `B`.

        Parameters
        ----------
        f_parser : Parser[Callable[[A], B]]
            the converting function

        Returns
        -------
        Callable[[Parser[A]], Parser[B]]
            the parser for an object of type B
        """

        return f_parser.and_then(self).map(lambda fn_and_a: fn_and_a[0](fn_and_a[1]))

    def optional(self: Parser[A], default: A | None = None) -> Parser[list[A]]:
        """
        Parse 0 or 1 time.

        Returns
        -------
        Parser[list]
            Parser that parses A 0 or 1 time.
        """

        def parse_fn(s: Stream) -> ParseResult[list[A]]:
            result = self(s)
            match result:
                case ParseSuccess(loc=loc, val=val, rs=rs):
                    return ParseSuccess(loc=loc, val=[val], rs=rs)
                case ParseFailure(loc=loc):
                    return ParseSuccess(
                        loc, [default] if default is not None else [], s
                    )
                case _:  # pragma: no cover
                    raise InternalError()

        return Parser(parse_fn, label=f"optional {self.label}")

    def _many0_recur(self: Parser[A], s: Stream) -> tuple[list, Stream]:
        first_result = self(s)
        match first_result:
            case ParseFailure():
                return ([], s)
            case ParseSuccess(val=first_val, rs=first_rs):
                (  # pylint: disable=unpacking-non-sequence
                    follow_vals,
                    rs,
                ) = self._many0_recur(first_rs)
                return ([first_val] + list(follow_vals), rs)
        raise InternalError()

    def many0(self) -> Parser[list]:
        """
        Parses 0 or more times

        Returns
        -------
        Parser[list]
            Parser that parses A 0 or more times
        """

        def parse_fn(s: Stream) -> ParseResult[list]:
            val, rs = self._many0_recur(s)  # pylint: disable=unpacking-non-sequence
            match s.head():
                case (_, Location(line=line, col=col)):
                    return ParseSuccess(Location(line=line, col=col), val, rs)
                case _:
                    return ParseFailure(
                        loc=s.loc[-1],
                        label=f"zero or more {self.label}",
                        msg="stream exhausted",
                    )

        return Parser(
            parse_fn,
            label=f"zero or more {self.label}",
        )

    def many1(self) -> Parser[list]:
        """
        Parses 1 or more times

        Returns
        -------
        Parser[list]
        """

        def parse_fn(s: Stream) -> ParseResult[list]:
            first_result = self(s)
            match first_result:
                case ParseFailure():
                    return first_result
                case ParseSuccess(loc=loc_first, val=first_val, rs=first_rs):
                    (  # pylint: disable=unpacking-non-sequence
                        follow_vals,
                        rs,
                    ) = self._many0_recur(first_rs)
                    return ParseSuccess(
                        loc=loc_first, val=[first_val] + list(follow_vals), rs=rs
                    )
                case _:  # pragma: no cover
                    raise InternalError()

        return Parser(parse_fn, label=f"one or more {self.label}")

    def many1_sep_by(self: Parser[A], sep_parser: Parser) -> Parser[list[A]]:
        """
        Parses 1 or more times with separator

        Parses A 1 or more times with a separator between each pair of occurences.

        Parameters
        ----------
        val_parser : Parser[A]
            parser for the value
        sep_parser : Parser
            parser for the separator

        Returns
        -------
        Parser[list[A]]
        """
        sep_and_val_parser = sep_parser.bind(lambda _: self)
        follow_parser = sep_and_val_parser.many0()
        parser = self.bind(
            lambda first_val: follow_parser.map(
                lambda follow_vals: [first_val] + follow_vals
            )
        )
        return parser.set_label(
            f"one or more {self.label} separated by {sep_parser.label}"
        )

    def many0_sep_by(self: Parser[A], sep_parser: Parser) -> Parser[list[A]]:
        """
        Parses 0 or more times with separator

        Parses A 0 or more times with a separator between each pair of occurences.

        Parameters
        ----------
        sep_parser : Parser
            parser for the separator

        Returns
        -------
        Parser[list[A]]
        """
        return (
            self.many1_sep_by(sep_parser)
            .or_else(self.map(lambda a: [a]))
            .set_label(f"zero or more {self.label} separated by {sep_parser.label}")
        )

    def preceded_by(self: Parser[A], other: Parser) -> Parser[A]:
        """
        Parses A preceded by something

        Parameters
        ----------
        other : Parser
            parser for the thing preceding A

        Returns
        -------
        Parser[A]
        """
        return (other & self).map(lambda pair: pair[1])

    def succeeded_by(self: Parser[A], other: Parser) -> Parser[A]:
        """
        Parses A preceded by something

        Parameters
        ----------
        other : Parser
            parser for the thing succeeding A

        Returns
        -------
        Parser[A]
        """
        return (self & other).map(lambda pair: pair[0])

    def surrounded_by(self: Parser[A], lparser: Parser, rparser: Parser) -> Parser[A]:
        """
        Parses A surrounded by two other things

        Parameters
        ----------
        lparser : Parser
            parser for the left thing

        rparser : Parser
            parser for the right thing

        Returns
        -------
        Parser[A]
        """
        return self.preceded_by(lparser).succeeded_by(rparser)

    def times(self: Parser[A], n: int) -> Parser[list[A]]:
        """
        Parses A exactly `n` times

        Parameters
        ----------
        n : int
            return

        Returns
        -------
        Parser[A]
        """
        label = f"({self.label}) {n} times"

        def parse_fn(s: Stream) -> ParseResult[list]:
            parse_many1_result = self.many1()(s)
            match parse_many1_result:
                case ParseSuccess(loc=loc, val=la, rs=rs):
                    if len(la) == n:
                        return ParseSuccess(loc=loc, val=la, rs=rs)
                    else:
                        head = s.head()
                        if head is not None:
                            _, loc = head
                            return ParseFailure(loc=loc, label=self.label, msg="")
                        else:
                            raise InternalError()
                case ParseFailure():
                    failure: ParseFailure = parse_many1_result
                    return ParseFailure(loc=failure.loc, label=label, msg=failure.msg)
                case _:  # pragma: no cover
                    raise InternalError()

        return Parser(parse_fn, label=label)

    @staticmethod
    def satisfy(
        predicate: Callable[[str], bool], *, label: str = "satisfy"
    ) -> Parser[str]:
        """
        Parser that parses the next character if the predicate is `True`

        Parameters
        ----------
        predicate : Callable[[str], bool]
            The condition on which the next character is parsed or not.
        label : str
            The label of the parser.

        Returns
        -------
        Parser[str]
        """

        def parse_fn(s: Stream) -> ParseResult[str]:
            head = s.head()
            if head is not None:
                c, loc = head
                if predicate(c):
                    return ParseSuccess(loc=loc, val=c, rs=s.tail())
                else:
                    return ParseFailure(
                        loc=loc,
                        label=label,
                        msg=f"unexpected character '{c}'",
                    )
            else:
                return ParseFailure(
                    loc=s.loc[-1],
                    label=label,
                    msg="input stream exhausted",
                )

        return Parser(parse_fn, label=label)

    @staticmethod
    def char(char: str) -> Parser[str]:
        """
        Parser for a single character

        Parameters
        ----------
        char : str
            the character to parse

        Returns
        -------
        Parser[str]
        """
        return Parser.satisfy(lambda c: c == char, label=f"char '{char}'")

    @staticmethod
    def until(predicate: Callable[[str], bool], label: str = "until") -> Parser[str]:
        """
        Parser that parses until a predicate is true

        Parameters
        ----------
        label : str
            the label of the parser
        predicate : Callable[[str], bool]
            the condition on which the parser stops

        Returns
        -------
        Parser[str]
        """
        return (
            Parser.satisfy(lambda c: not predicate(c))
            .many0()
            .map("".join)
            .set_label(label)
        )

    @staticmethod
    def sequence(parsers: Iterable[Parser]) -> Parser[list]:
        """
        Parser for a sequence of things

        Parameters
        ----------
        parsers : Iterable[Parser]
            A sequence of parsers

        Returns
        -------
        Parser[list]
        """

        def chain_list_parsers(
            seq_a_parser: Parser[list],
            seq_b_parser: Parser[list],
        ) -> Parser[list]:
            """
            Chain two iterable parsers together to form a single iterable parser
            """
            parser = seq_a_parser.and_then(seq_b_parser)

            def parse(s: Stream) -> ParseResult[list]:
                result = parser(s)
                match result:
                    case ParseSuccess(loc=loc, val=(seq_a, seq_b), rs=rs):
                        return ParseSuccess(
                            loc=loc,
                            val=list(chain(seq_a, seq_b)),
                            rs=rs,
                        )
                    case ParseFailure():
                        return result
                    case _:  # pragma: no cover
                        raise InternalError()

            return Parser(parse, label=f"{seq_a_parser}, {seq_b_parser}")

        list_singleton_parsers: Iterable[Parser] = map(
            lambda parser: parser.map(lambda obj: [obj]), parsers
        )
        parser: Parser[list] = reduce(
            chain_list_parsers,
            list_singleton_parsers,
        )
        return parser.set_label(f"sequence of ({parser.label})")

    @staticmethod
    def choice(parsers: Iterable[Parser]) -> Parser:
        """
        Parser that parses the first matching alternative

        Parser for a list of alternatives. The first matching alternative is parsed.

        Parameters
        ----------
        parsers : Iterable[Parser]
            A sequence of parsers for the alternatives

        Returns
        -------
        Parser
        """

        def chain_parsers(p_a: Parser, p_b: Parser) -> Parser:
            return p_a.or_else(p_b).set_label(f"{p_a.label}, {p_b.label}")

        parser = reduce(chain_parsers, parsers)
        parser.set_label(f"choice of ({parser.label})")
        return parser

    @staticmethod
    def just(a: A) -> Parser[A]:
        """
        A parser that always parses successfully and returns the desired value without
        affecting the parse stream

        Parameters
        ----------
        a : A
            the value

        Returns
        -------
        Parser[A]
            A parser that always successfully parses the value while keeping the parse
            stream unchanged
        """

        def parse_fn(s: Stream):
            head = s.head()
            if head is not None:
                _, loc = head
            else:
                loc = s.loc[-1] if len(s.loc) > 0 else Location(0, 0)
            return ParseSuccess(loc=loc, val=a, rs=s)

        return Parser(parse_fn, label=f"{a}")

    @staticmethod
    def string(literal: str) -> Parser[str]:
        """
        Parser that parses a string literal

        Parameters
        ----------
        literal : str
            The string literal

        Returns
        -------
        Parser[str]
        """
        char_parsers = map(Parser.char, literal)
        return (
            Parser.sequence(char_parsers).map("".join).set_label(f"literal {literal}")
        )

    @staticmethod
    def digit() -> Parser[str]:
        """
        Parser that parses a digit

        Returns
        -------
        Parser[str]
        """
        return Parser.satisfy(lambda c: c in string.digits).set_label("digit")

    @staticmethod
    def digit_nonzero() -> Parser[str]:
        """
        Parser that parses a nonzero digit

        Returns
        -------
        Parser[str]
        """
        return Parser.satisfy(lambda c: c in string.digits and c != "0").set_label(
            "digit_nonzero"
        )

    @staticmethod
    def ascii_lowercase() -> Parser[str]:
        """
        Parser that parses a lowercase ASCII character

        Returns
        -------
        Parser[str]
        """
        return Parser.satisfy(lambda c: c in string.ascii_lowercase).set_label(
            "ascii_lowercase"
        )

    @staticmethod
    def ascii_uppercase() -> Parser[str]:
        """
        Parser that parses a lowercase ASCII character

        Returns
        -------
        Parser[str]
        """
        return Parser.satisfy(lambda c: c in string.ascii_uppercase).set_label(
            "ascii_uppercase"
        )

    @staticmethod
    def ascii() -> Parser[str]:
        """
        Parser that parses an ASCII character

        Returns
        -------
        Parser[str]
        """
        return (
            Parser.ascii_lowercase()
            .or_else(Parser.ascii_uppercase())
            .set_label("ascii")
        )
