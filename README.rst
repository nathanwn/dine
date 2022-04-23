dine: Parser Combinator Library
======================================

.. start-inclusion-marker-badges

.. image:: https://img.shields.io/github/workflow/status/nathan-wien/dine/Test?style=flat-square
    :alt: Build Status
    :target: https://github.com/nathan-wien/dine/actions?query=workflow%3ATest

.. image:: https://codecov.io/gh/nathan-wien/dine/branch/main/graph/badge.svg
    :alt: Coverage
    :target: https://codecov.io/gh/nathan-wien/dine

.. image:: https://img.shields.io/badge/python%20version-%3E=3.10-02ad93.svg?style=flat-square
    :alt: Python Version
    :target: https://www.python.org/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code Style
    :target: https://github.com/psf/black

.. end-inclusion-marker-badges


Contents
------------------------
.. contents:: This README includes the following sections


Introduction
--------------------

**dine** is a Parser Combinator Library targeting Python >=3.10.


Development
--------------------

- Create a virtual environment for the project:

.. code-block:: console

    $ python3 -m venv .venv
    $ source .venv/bin/activate

- Update pip

.. code-block:: console

    $ pip install --upgrade pip

- Install `dine` in editable mode to expose its API:

.. code-block:: console

    $ pip install -e .

- Install dev dependencies:

.. code-block:: console

    $ pip install -r requirements/requirements_tests.txt
