#!/usr/bin/env bash

sphinx-apidoc -o . ../src/dine
make html
