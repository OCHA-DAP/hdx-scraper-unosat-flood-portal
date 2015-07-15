#!/usr/bin/python
# -*- coding: utf-8 -*-

# system
import os
import sys
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(dir, 'scripts'))

# testing
import mock
import unittest
from mock import patch

# program
import config.load as Confi
#
# Global variables.
#
TEST_DATA = 'test_flood_portal_output.json'

# class CheckConfigFile(unittest.TestCase):
#   '''Unit tests for checking if the config file is organized correctly.'''

#   ## Structural tests.
#   def test_wrapper_database_function_works(self):
#     assert DB.Main() != False
