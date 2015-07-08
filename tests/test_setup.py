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
import config.load as Config
import config.database as DB

#
# Global variables.
#
TEST_DATA = 'test_flood_portal_output.json'

class CheckConfigurationStructure(unittest.TestCase):
  '''Unit tests for the configuration files.'''

  def test_that_load_config_fails_gracefully(self):
    assert Config.LoadConfig('xxx.json') == False

  ## Object type tests.
  def test_config_is_list(self):
    dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
    d = Config.LoadConfig(os.path.join(dir, 'config', 'dev.json'))
    assert type(d) is list

  def test_config_returns_a_table_list(self):
    dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
    d = Config.LoadConfig(os.path.join(dir, 'config', 'dev.json'))
    t = d[0]['database']['fields']
    assert type(t) is list


class CheckDatabaseCreation(unittest.TestCase):
  '''Unit tests for the setting up the database.'''

  ## Structural tests.
  def test_wrapper_database_function_works(self):
    assert DB.Main() != False
