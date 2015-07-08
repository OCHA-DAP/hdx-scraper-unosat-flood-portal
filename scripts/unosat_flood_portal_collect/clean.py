#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import json

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import config.load as Config
from datetime import datetime
from countrycode import countrycode
from utilities.db import CleanTable
from utilities.db import StoreRecords
from utilities.db import ReadAllRecords
from utilities.prompt_format import item


def CleanDates(data, verbose=False):
  '''Find and clean date entries from the title of datasets.'''

  #
  # Check the title of each record
  # and transform the dates into ISO.
  #
  print '%s Processing dates.' % item('prompt_bullet')
  record_array = []
  for record in data:
    s = record['title']
    try:
      d = datetime.strptime(s[s.find("(")+1:s.find(")")], '%d %B %Y')

    except Exception as e:
      if verbose:
        print '%s Could not convert date for: %s' % (item('prompt_error'), s)
        print e

      #
      # Adding None if
      # fails to convert.
      #
      record['created'] = None

    record['created'] = d.strftime('%Y-%m-%d')
    record_array.append(record)


  return record_array


def IdentifyCountries(data, verbose=True):
  '''Idenfiying a country code based on a string.'''

  print '%s Identifying countries.' % item('prompt_bullet')
  #
  # Check the description of each
  # record find an ISO-3-letter-code.
  #
  record_array = []
  for record in data:
    s = record['summary']
    try:
      d = countrycode(codes=str(s), origin='country_name', target='iso3c')

    except Exception as e:
      if verbose:
        print '%s Could not identify country for: %s' % (item('prompt_error'), s)
        print e

      #
      # Adding None if fails
      # to identify country.
      #
      record['country'] = None

    #
    # In case the output
    # isn't an ISO-3-letter-code.
    #
    if len(d) == 3:
      record['country'] = d

    else:
      record['country'] = None

    record_array.append(record)


  return record_array
