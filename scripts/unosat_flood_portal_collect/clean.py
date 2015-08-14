#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import json
import requests

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import config.load as Config
from datetime import datetime
from countrycode import countrycode
from utilities.db import CleanTable
from utilities.db import StoreRecords
from utilities.db import ReadAllRecords
from utilities.prompt_format import item


def CleanDates(data, verbose=False, test=False):
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

      if test:
        return False

      #
      # Adding None if
      # fails to convert.
      #
      record['created'] = None

    record['created'] = d.strftime('%m/%d/%Y')
    record_array.append(record)


  return record_array



def IdentifyCountries(data, verbose=False, test=False):
  '''Idenfiying a country code based on a string.'''

  print '%s Identifying countries.' % item('prompt_bullet')
  #
  # Check the description of each
  # record find an ISO-3-letter-code.
  #
  record_array = []
  for record in data:
    try:
      s = record['summary']
      d = countrycode(codes=str(s), origin='country_name', target='iso3c')

    #
    # A bit of a horrible hack,
    # but these lines needed testing.
    #
    except Exception as e:
      if test:
        try:
          print s
        except NameError:
          s = None

      if verbose:
        print '%s Could not identify country for: %s' % (item('prompt_error'), str(s))
        print e

      if test:
        return False

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



def CleanTitle(data, verbose=True):
  '''Cleaning titles.'''

  print '%s Cleaning title.' % item('prompt_bullet')

  record_array = []
  for record in data:
    summary = record['summary']
    title = record['title']

    #
    # Finds the date stamp.
    #
    t = '(' + title[title.find("(")+1:title.find(")")] + ')'

    #
    # Extracts title from description.
    #
    find = re.compile(r"^[^.]*")
    m = re.match(find, summary)
    c = m.group(0)

    #
    # Merges both results
    #
    merged_title = c[c.find('of the ')+7:c.find(' which began ')] + ' ' + t

    #
    # Cleaning the original title.
    #
    # clean = s[14:]  # eliminating leading crisis code
    # t = '(' + clean[clean.find("(")+1:clean.find(")")] + ')'
    # clean = clean.replace(t, '')

    #
    # Appending clean record.
    #
    record['title'] = merged_title
    record_array.append(record)


  return record_array



def IdentifyFileTypeAndFileName(data, verbose=True):
  '''Identify a file type of a resource.'''

  print '%s Identifying file extension.' % item('prompt_bullet')

  record_array = []
  for record in data:

    #
    # Extracting file extension from href.
    # Also cleans preceeding period and
    # makes string upper case.
    #
    href = record['link_href']
    file_extension = os.path.splitext(href)[1].replace('.', '').upper()
    file_name = os.path.basename(href)

    #
    # Checking if it is known.
    # If not, store None.
    #
    if len(file_extension) > 3 or len(file_extension) == 0:
      file_extension = None
      file_name = None

    #
    # Store and append.
    #
    record['file_extension'] = file_extension
    record['file_name'] = file_name
    record_array.append(record)

  return record_array
