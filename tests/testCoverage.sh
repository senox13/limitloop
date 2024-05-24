#!/usr/bin/env bash

python3 -m coverage run limitloopTests.py
python3 -m coverage report
python3 -m coverage erase

