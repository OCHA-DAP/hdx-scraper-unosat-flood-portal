#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import schedule

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from utilities.prompt_format import item
from unosat_flood_portal_collect import collect as Collect

def Wrapper(patch=False):
  '''Wrapper for main program.'''

  #
  # Collect data.
  #
  Collect.Main(patch=True)


#
# Setting-up schedule.
#
schedule.every(1).day.do(Wrapper)


def Main(verbose=True):
  '''Wrapper to run all the scheduled tasks.'''

  if verbose:
    print '%s Running scheduler.' % item('prompt_bullet')

  while True:
    schedule.run_pending()
    time.sleep(1)


if __name__ == '__main__':
  Main()
