#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import scraperwiki

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import config.load as Config
from utilities.prompt_format import item
from unosat_flood_portal_collect import collect
from unosat_flood_portal_collect import export


if __name__ == '__main__':

  #
  # TODO: allow for the
  # setting of the dev config file
  # here.
  #
  try:
    sys.argv[1]
    config_path = Config.DEV_CONFIG_PATH
    print "%s Running in development mode." % item('prompt_warn')

  except IndexError:
    config_path = Config.PROD_CONFIG_PATH
  

  #
  # Collect and export data.
  #
  try:
    collect.Main(patch=True)
    export.Main()
    scraperwiki.status('ok')
    print '%s ScrapeWiki Status: Collected data successfully.' % item('prompt_succes')


  except Exception as e:
    print e
    scraperwiki.status('error', 'Error collecting data.')
    os.system("mail -s 'UNOSAT Flood Portal: Failed to collect data.' luiscape@gmail.com")

