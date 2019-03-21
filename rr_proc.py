#!/usr/bin/env python
"""
Author: Max Solomcuk, max.solomcuk@cgi.com
Request and response processing for USGS API Client
"""

import logging
import logging.config
import requests
from threading import Thread
import yaml

with open('logging.conf', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)

def search_to_dl_opts(in_file, out_file, dataset_name='LANDSAT_8_C1'):
    """
    Read a response from search query, extract entityIds and write out to a "downloadoptions" conf file.
    """
    with open(in_file, 'r') as f:
        sr = yaml.load(f)
    results = sr['results']
    entityIds = [r['entityId'] for r in results]
    output = {}
    output['datasetName'] = dataset_name
    output['entityIds'] = entityIds
    print(output)
    with open(out_file, 'w') as f:
        yaml.dump(output, f, default_flow_style=False)

def search_to_dl(in_file, out_file, dataset_name='LANDSAT_8_C1', prod_types=['FR_BUND', 'STANDARD']):
    """
    Read a response from search query, extract entityIds and write out to a "download" conf file.
    """
    with open(in_file, 'r') as f:
        sr = yaml.load(f)
        results = sr['results']
    entityIds = [r['entityId'] for r in results]
    output = {}
    output['datasetName'] = dataset_name
    output['products'] = prod_types
    output['entityIds'] = entityIds
    print(output)
    with open(out_file, 'w') as f:
        yaml.dump(output, f, default_flow_style=False)