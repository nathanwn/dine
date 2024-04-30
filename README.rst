.. start-inclusion-marker-header

dine: Parser Combinator Library
======================================


.. image:: https://img.shields.io/github/actions/workflow/status/nathan-wien/dine/test.yml?branch=main
    :alt: Build Status
    :target: https://img.shields.io/github/actions/workflow/status/nathan-wien/dine/test.yml?branch=main

.. image:: https://codecov.io/gh/nathanwn/dine/branch/main/graph/badge.svg
    :alt: Coverage
    :target: https://codecov.io/gh/nathanwn/dine

.. image:: https://img.shields.io/badge/python%20version-%3E=3.10-02ad93.svg?style=flat-square
    :alt: Python Version
    :target: https://www.python.org/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code Style
    :target: https://github.com/psf/black


Introduction
--------------------

**dine** is a `Parser Combinator <https://en.wikipedia.org/wiki/Parser_combinator>`_ Library targeting Python >=3.10.

.. end-inclusion-marker-header


.. start-inclusion-marker-readme-content


Quick Start
--------------------

Requirements
~~~~~~~~~~~~~~~~~~~~

* Python 3.10


Installation
~~~~~~~~~~~~~~~~~~~~

At the moment, the project has not been published to `pypi <https://pypi.org/>`_. You can instead install it directly from github as follows:

.. code-block:: console

    $ python -m pip install git+https://github.com/nathan-wien/dine.git


Usage
~~~~~~~~~~~~~~~~~~~~

Basics
^^^^^^^^^^^^^^

Using the ``dine.parser.Parser`` class, you can create parsing functors. Functors are object that can be called like functions.

When called, each parsing functor (or parser for short) can accept either:

* a builtin ``str`` object,  or
* a ``dine.parser.Stream`` object.

The parser then returns an object of base class ``dine.result.ParseResult``, which can either be:

* A ``ParseSuccess(loc, val, rs)`` object if the parser parses successfully, where:

  * ``loc: dine.stream.Location`` is the parsed location (line and column) in the initial stream,
  * ``val`` is the parsed value, and
  * ``rs: dine.stream.Stream`` is the remaining stream after applying the parser.

* A ``ParseFailure(loc, label, msg)`` object if the parser fails to parse, where:


  * ``loc: dine.stream.Location`` is the location (line and column) in the initial stream where the parser (first) fails to parse,
  * ``label: str`` the label of the parser that fails to parse, and
  * ``msg: str`` is the error message.


.. code-block:: python

    >>> from dine.parser import Parser

    # functor that parses a digit
    >>> digit_parser = Parser.digit()
    >>> digit_parser('42')
    ParseSuccess(
        loc=(line=1,col=1),
        val='4',
        rs=Stream("2")
    )
    >>> digit_parser('hi')
    ParseFailure(
        loc=(line=1,col=1),
        label='digit',
        msg="unexpected character 'h'"))
    )

    # functor that parses a lowercase ASCII character
    >>> lowercase_parser = Parser.ascii_lowercase()
    >>> lowercase_parser('abc')
    ParseSuccess(
        loc=(line=1,col=1),
        val='a',
        rs=Stream("bc")
    )
    >>> lowercase_parser('ABC')
    ParseFailure(
        loc=(line=1,col=1),
        label='dine.parser.Parser.ascii_lowercase',
        msg="unexpected character 'A'"))
    )


Combinators
^^^^^^^^^^^^^^

It is not a parser combinator library without the ability of combining parsers together to create more complex parsers.

The following shows some combinators that ``dine`` offers. For an exhaustive list of combinator, please refer to the `documentation <https://dine.readthedocs.io/en/latest/index.html>`_.


.. code-block:: python

    >>> from dine.parser import Parser

    # apply a parser after the other
    >>> Parser.char('a').and_then(Parser.char('b'))('ab$')
    ParseSuccess(
        loc=(line=1,col=1),
        val=('a', 'b'),
        rs=Stream("$")
    )
    # alternatively
    >>> (Parser.char('a') & Parser.char('b'))('ab$')
    ParseSuccess(
        loc=(line=1,col=1),
        val=('a', 'b'),
        rs=Stream("$")
    )

    # apply another parser if the first one fails
    >>> Parser.char('a').or_else(Parser.char('b'))('ab$')
    ParseSuccess(
        loc=(line=1,col=1),
        val='a',
        rs=Stream("b$")
    )
    # alternatively
    >>> (Parser.char('a') | Parser.char('b'))('ab$')
    ParseSuccess(
        loc=(line=1,col=1),
        val='a',
        rs=Stream("b$")
    )

    # parse 1 or more digits
    >>> digits_parser = Parser.digit().many1()
    >>> digits_parser('123abc')
    ParseSuccess(
        loc=(line=1,col=1),
        val=['1', '2', '3'],
        rs=Stream("abc")
    )

    # You can convert the parsed value (the `val` field in a `ParsedSuccess` object)
    # to anything you want using the `map` method. For example:
    >>> num_parser = digits_parser.map(lambda digit_list: int("".join(digit_list)))
    >>> num_parser('123abc')
    ParseSuccess(
        loc=(line=1,col=1),
        val=123,
        rs=Stream("abc")
    )

    # Parser that sequences a bunch of parsers, one after the other
    >>> abc_parser = Parser.sequence(
    ...     [Parser.char('a'), Parser.char('b'), Parser.char('c')]
    ... ).set_label('abc_parser')

    >>> abc_parser('abc$')
    ParseSuccess(
        loc=(line=1,col=1),
        val=['a', 'b', 'c'],
        rs=Stream("$")
    )

    >>> abc_parser('$')
    ParseFailure(
        loc=(line=1,col=1),
        label='abc_parser',
        msg="unexpected character '$'"))
    )

    # Parser that parses a bunch of alternatives
    >>> oneof_abc_parser = Parser.choice(
    ...     [Parser.char('a'), Parser.char('b'), Parser.char('c')]
    ... ).set_label('oneof_abc_parser')

    >>> oneof_abc_parser('c$')
    ParseSuccess(
        loc=(line=1,col=1),
        val='c',
        rs=Stream("$")
    )

    >>> oneof_abc_parser('d$')
    ParseFailure(
        loc=(line=1,col=1),
        label='oneof_abc_parser',
        msg="unexpected character 'd'"))
    )

    # Parsers that throw away things
    >>> Parser.char('b').preceded_by(Parser.string("@"))("@b$")
    ParseSuccess(
        loc=(line=1,col=1),
        val='b',
        rs=Stream("$")
    )

    >>> Parser.char('b').succeeded_by(Parser.string("@"))("b@$")
    ParseSuccess(
        loc=(line=1,col=1),
        val='b',
        rs=Stream("$")
    )

    # Parser that parses a list of numbers separated by commas
    >>> comma_parser = Parser.char(',')
    >>> num_list_parser = num_parser.many1_sep_by(comma_parser)
    >>> num_list_parser('5,15,250,1000')
    ParseSuccess(
        loc=(line=1,col=1),
        val=[5, 15, 250, 1000],
        rs=Stream("")
    )


Documentation
---------------------

The full documentation can be found `here <https://dine.readthedocs.io/en/latest/index.html>`_. The documentation will be updated with more details and examples in the future.


FAQ/You may ask
--------------------

* Why is the minimum python version compatible with this library is 3.10?

  * The implementation of this library makes heavy use of the structural pattern matching (a.k.a. ``match`` statement) feature, which is only available on python 3.10 or later.


Acknowledgements/Inspirations
---------------------------------

* The `COMP4403 <https://my.uq.edu.au/programs-courses/course.html?course_code=COMP4403>`_ course (Compilers and Interpreters) at the University of Queensland.
* Scott Wlaschin's `talk on parser combinator <https://youtu.be/RDalzi7mhdY>`_ and `his blog posts <https://fsharpforfunandprofit.com/series/understanding-parser-combinators/>`_ on the topic.
* Max Bo's `Parser Combinator Talk <https://youtu.be/bvjBgAGq3E8>`_ at UQCS.

.. end-inclusion-marker-readme-content
