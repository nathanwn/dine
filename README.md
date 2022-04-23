<div align="center">

  <h1>dine</h1>
  <h5>Parser Combinator Library for Python >= 3.10</h5>

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/nathan-wien/dine/Test?style=flat-square)](https://github.com/nathan-wien/dine/actions?query=workflow%3ATest)
![Python Version](https://img.shields.io/badge/python%20version-%3E=3.10-02ad93.svg?style=flat-square)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

# dine

**dine** is a parser combinator library targeting Python 3.10+.

## Setup Development Environment

- Create a virtual environment for the project:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

- Update pip

```sh
pip3 install --upgrade pip
```

- Install packages (including dev dependencies) and `dine` to expose its API to the `tests` directory:

```
pip3 install -e ".[dev]"
```
