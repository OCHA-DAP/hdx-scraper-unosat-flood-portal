#!/bin/bash

#
# Installing dependencies.
#
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install nose  # for tests

#
# Running collector-specific setup scripts.
#
python scripts/setup/