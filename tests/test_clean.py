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
import unosat_flood_portal_collect.clean as Clean


class CheckCleanScriptsWork(unittest.TestCase):
  '''Unit tests checking if the cleaning scritps are working as expected.'''

  def test_clean_dates_parses_dates_correctly(self):
    c = [{ 'title': 'Title of Dataset (03 August 2015)' }]  # correct
    w = [{ 'title': 'Title of Dataset (05/06/2014)' }]  # incorrect
    w2 = [{ 'title': 'Title of Dataset (2015-01-02)' }]  # incorrect
    assert Clean.CleanDates(data=c,test=True) != False
    assert Clean.CleanDates(data=w,test=True) == False
    assert Clean.CleanDates(data=w2,verbose=True,test=True) == False

  def test_parsing_of_countries_work(self):
    c = [{ 'summary': 'Something was happening in Palestine.' }]  # country
    w = [{ 'xxx': 'Something was happening in Palestine.' }]  # error
    assert Clean.IdentifyCountries(data=c, verbose=True) != False
    assert Clean.IdentifyCountries(data=w, verbose=True, test=True) == False


  def test_cleaning_of_title_works(self):
    c = [{ 'title': 'Title of Dataset (03 August 2015)','summary': 'Something was happening in Palestine.' }]
    assert Clean.CleanTitle(data=c, verbose=True) != False

  def test_file_type_and_path_are_parsed_correctly(self):
    c = [{ 'link_href': 'https://unosatgis.cern.ch/arcgis/rest/services/FP02/FP02_FL_20150730_VNM_20150803_Flood_TerraSARX/MapServer/kml/mapImage.kmz' }]
    assert Clean.IdentifyFileTypeAndFileName(data=c, verbose=True) != False
