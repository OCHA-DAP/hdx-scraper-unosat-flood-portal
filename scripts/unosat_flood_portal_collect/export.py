#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
import scraperwiki
from copy import copy
from datetime import datetime

dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)


from utilities.prompt_format import item


def ExportDatasets(directory=None):
  '''Function to export datasets in a JSON format.'''

  print '%s Exporting Datasets JSON to disk.' % item('prompt_bullet')
  
  #
  # Sanity check.
  #
  if directory == None:
  	print '%s Provide a directory.' % (item('prompt_error'))

  #
  # Loading records from database.
  #
  cursor = scraperwiki.sqlite.execute('SELECT * FROM processed_data GROUP BY hdx_dataset_id')
  records = cursor['data']

  #
  # Default dataset.
  #
  default_dataset = { 
    'name': None,
    'title': None,
    'owner_org': 'un-operational-satellite-appplications-programme-unosat',  # default for UNOSAT 
    'author': 'unosat',
    'author_email': 'emergencymapping@unosat.org',  # default for UNOSAT
    'maintainer': 'unosat',  # default for UNOSAT
    'maintainer_email': 'emergencymapping@unosat.org',  # default for UNOSAT
    'license_id': 'hdx-other',  # default for UNOSAT
    'license_other': 'Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License',  # default for UNOSAT
    'dataset_date': None,  # has to be in MM/DD/YYYY format.
    'subnational': 1,  # has to be 0 or 1. Default 1 for UNOSAT.
    'notes': None,
    'caveats': 'This is a preliminary assessment and has not yet been validated in the field. It is important to consider the characteristics of the source imagery used in the analyses when interpreting results. For damage assessments it should be noted that only significant damage to the structural integrity of the buildings analyzed can be seen in imagery, while minor damage such as cracks or holes may not be visible at all. For flood extractions using radar data it is important to note that urban areas and highly vegetated areas may mask the flood signature and result in underestimation of flood waters. Users with specific questions or concerns should contact unosat@unitar.org to seek clarification.',
    'methodology': 'Other',  # default for UNOSAT
    'methodology_other': 'UNOSAT datasets and maps are produced using a variety of methods. In general, analysts closely review satellite imagery, often comparing two or more images together, and determine notable changes between the images. For damage assessments, refugee or IDP assessments, and similar analyses, these changes are then manually documented in the vector data by the analyst. For flood extractions, landcover mapping and similar analyses, a variety of automated remote sensing techniques are used to extract the relevant information which is then reviewed and revised as necessary by the analyst. In all cases, resulting data is then loaded into a standardized UNOSAT geodatabase and exported asshapefiles for dissemination.',
    'dataset_source':'UNOSAT',
    'package_creator': 'unosat',
    'private': False,  # has to be True or False
    'url': None,
    'state': 'active',  # always "active"
    'tags': [],  # has to be a list with {'name': None}
    'groups': []  # has to be ISO-3-letter-code. {'id': None}
    }
  
  data = []
  for record in records:

    t = default_dataset
  
    #
    # Adding fields from records.
    #
    t['title'] = record['title']
    t['name'] = record['hdx_dataset_id']
    t['dataset_date'] = record['created']
    t['notes'] = record['summary']

    #
    # Adding tags and country.
    #
    t['tags'] = [{ 'name': record['crisis_code'] }, { 'name': 'geodata' }]
    t['groups'] = [{ 'id': str(record['country']).lower() }]


    #
    # Appending results.
    #
    data.append(copy(t))
 
  #
  # Write JSON to disk.
  #
  with open(os.path.join(directory, 'datasets.json'), 'w') as outfile:
    json.dump(data, outfile)



def ExportResources(directory=None):
  '''Export the UNOSAT resources for their respective datasets.'''

  print '%s Exporting Resources JSON to disk.' % item('prompt_bullet')


  #
  # Sanity check.
  #
  if directory == None:
    print '%s Provide a directory.' % (item('prompt_error'))

  #
  # Loading records from database.
  #
  cursor = scraperwiki.sqlite.execute('SELECT * FROM processed_data')
  records = cursor['data']


  #
  # Default resource.
  #
  default_resource = {
    "package_id": None,
    "url": None,
    "name": None,
    "format": None,
    "description": None  # file size could go here. 
  }

  data = []
  for record in records:

    t = default_resource
  
    #
    # Adding fields from records.
    #
    t['package_id'] = record['hdx_dataset_id']
    t['url'] = record['link_href']
    t['name'] = record['file_name']
    t['format'] = record['file_extension']

    #
    # Appending results.
    #
    data.append(copy(t))
 
  #
  # Write JSON to disk.
  #
  with open(os.path.join(directory, 'resources.json'), 'w') as outfile:
    json.dump(data, outfile)



def ExportGalleryItems(directory=None, verbose=True):
  '''Fetches the gallery items from UNOSAT and exports the necessary JSON file.'''

  #
  # Gallery items need both an image
  # and an URL to wich to point.
  #
  print '%s Exporting Gallery Item JSON to disk.' % item('prompt_bullet')

  #
  # Sanity check.
  #
  if directory == None:
    print '%s Provide a directory.' % (item('prompt_error'))

  #
  # Loading records from database.
  #
  cursor = scraperwiki.sqlite.execute("SELECT * FROM processed_data WHERE link_type='open' GROUP BY hdx_dataset_id")
  records = cursor['data']

  #
  # Default resource.
  #
  default_gallery = {
   "title": "Map Preview",
   "type": "app",
   "description": "Map preview on ArcGIS online.",
   "url": None,
   "image_url": None,
   "dataset_id": None
  }

  data = []
  for record in records:

    t = default_gallery
  
    #
    # Adding fields from records.
    #
    t['dataset_id'] = record['hdx_dataset_id']

    try:
      
      #
      # Extracting map id from URL.
      #
      l = record['link_href']
      arcgis_url = 'http://www.arcgis.com/home/webmap/viewer.html?url=' + l
      map_id = os.path.split(os.path.split(l)[0])[1]
      bounding_box_data = record['bbox']

      #
      # Assembling URL.
      #
      base_url = 'https://unosatgis.cern.ch/arcgis/rest/services/FP02/' + map_id
      bouding_box_url = '/MapServer/export?bbox=' + bounding_box_data + '&format=png&transparent=false&f=json'
      u = base_url + bouding_box_url
      
      #
      # Making request.
      #
      if verbose:
        print '%s Making request to: %s' % (item('prompt_bullet'), u)

      r = requests.get(u)

      if r.status_code != 200:
        if verbose:
          print '%s Could not make request to UNOSAT images.' % item('prompt_error')
        
        #
        # If have problems querying UNOSAT,
        # add None and continue.
        #
        # data.append(copy(t)
        # continue
      
      #
      # Fetch the image URL and store in record.
      #
      else:
        try:
          check = r.json()['error']['code']
          continue  # will not add gallery items without URL

        except Exception as e:
          t['image_url'] = r.json()['href']
          t['url'] = arcgis_url


    except Exception as e:
      if verbose:
        print '%s Could not make request to UNOSAT images.' % item('prompt_error')
        print e
    


    #
    # Appending results.
    #
    data.append(copy(t))
 
  #
  # Write JSON to disk.
  #
  with open(os.path.join(directory, 'gallery.json'), 'w') as outfile:
    json.dump(data, outfile)




def Main():
  '''Wrapper.'''
  
  #
  # Default directory.
  #
  data_dir = os.path.join(os.path.split(dir)[0], 'data')

  #
  # Calling JSON generators
  # to the default dir.
  #
  ExportDatasets(data_dir)
  ExportResources(data_dir)
  ExportGalleryItems(data_dir, verbose=False)

  print '%s Successfully exported JSON files.\n' % item('prompt_success')