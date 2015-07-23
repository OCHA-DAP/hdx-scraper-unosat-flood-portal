#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import yajl as json
import progressbar as pb

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from hdx_register import load
from hdx_register import delete
from hdx_register import create
from utilities.load import LoadConfig
from utilities.prompt_format import item
 

def Main():
  '''Wrapper'''

  p = LoadConfig(os.path.join(os.path.split(dir)[0], 'config', 'dev.json'))
  if p is not False:

    print "--------------------------------------------------"
    print '%s HDX Site: %s' % (item('prompt_bullet'), p['hdx_site'])

    #
    # Deleting all datasets from org.
    #
    if p['delete_datasets']:
      try:
        delete.DeleteAllDatasetsFromOrg(organization='un-operational-satellite-appplications-programme-unosat', hdx_site=p['hdx_site'], apikey=p['hdx_key'], verbose=p['verbose'])
      
      except Exception as e:
        print e
        return False

    try:
      #
      # Loading JSON data.
      #
      dataset_dict = load.LoadData(os.path.join(p['json_folder'], 'datasets.json'))
      resource_dict = load.LoadData(os.path.join(p['json_folder'], 'resources.json'))
      gallery_dict = load.LoadData(os.path.join(p['json_folder'], 'gallery.json'))

      # Delete resources before running:
      if p['delete_resources'] is True:
        delete.DeleteResources(dataset_dict=dataset_dict, hdx_site=p['hdx_site'], apikey=p['hdx_key'], verbose=p['verbose'])

      #
      # Create datasets, resources, and gallery items.
      #
      create.CreateDatasets(dataset_dict=dataset_dict, hdx_site=p['hdx_site'], apikey=p['hdx_key'], verbose=p['verbose'])
      create.CreateResources(resource_dict=resource_dict, hdx_site=p['hdx_site'], apikey=p['hdx_key'], verbose=p['verbose'])
      create.CreateGalleryItems(gallery_dict=gallery_dict, hdx_site=p['hdx_site'], apikey=p['hdx_key'], verbose=p['verbose'])


      print '%s Datasets registered in HDX successfully.\n' % item('prompt_success')

    except Exception as e:
      print e
      return False



if __name__ == '__main__':
  Main()