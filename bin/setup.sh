#!/bin/bash

#
# Installing dependencies.
#
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

#
# Running collector-specific setup scripts.
#
python scripts/config/
