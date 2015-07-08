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
import unosat_flood_portal_collect.collect as Collect

#
# Global variables.
#
TEST_DATA = 'test_flood_portal_output.json'

class CheckCollectorFunctions(unittest.TestCase):
  '''Unit tests checking if the collector is working as expected.'''

  def test_wrapper_doesnt_fail(self):
    assert Collect.Main() != False

  def test_fetch_data_function(self):
    assert Collect.FetchData(url='http://localhost:8080') == False

  def test_processing_works(self):
    data = Collect.DownloadAndProcessData()
    assert type(data) == list

  def test_clean_table_fails(self):
    assert Collect.CleanTable('foo') == False
