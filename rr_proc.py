#!/usr/bin/env python
"""
Author: Max Solomcuk, max.solomcuk@cgi.com
Request and response processing for USGS API Client
"""

import logging
import logging.config
import re
import os
import shutil
from datetime import datetime, timedelta
from queue import Queue
from threading import Thread

import requests
import yaml

#from homura import download

DISPLAYID_RE = r'L[COT]\d{2}_(L1GT|L1GS|L1TP)_\d{6}_\d{8}_\d{8}_\d{2}_(RT|T1|T2)'
MAX_DOWNLOADS = 10
abs_mod_dir = os.path.dirname(__file__)
TMP_PREFIX = "."
TMP_SUFFIX = "_lock"

with open(os.path.join(abs_mod_dir, 'logging.conf'), 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)

def search_to_dl_opts(in_file, out_file, dataset_name='LANDSAT_8_C1'):
    """
    Read a response from search query, extract entityIds and write out to a "downloadoptions" conf file.
    Assumes search() request was submitted with responseFormat = 'sceneList'.
    """
    with open(in_file, 'r') as f:
        sr = yaml.safe_load(f)
    #results = sr['results']
    #entityIds = [r['entityId'] for r in results]
    output = {}
    output['datasetName'] = dataset_name
    #output['entityIds'] = entityIds
    output['entityIds'] = sr['results']
    #print(output)
    with open(out_file, 'w') as f:
        yaml.dump(output, f, default_flow_style=False)

def search_to_dl(in_file, out_file, dataset_name='LANDSAT_8_C1', prod_types=['FR_BUND', 'STANDARD']):
    """
    Read a response from search query, extract entityIds and write out to a "download" conf file.
    Assumes search() request was submitted with responseFormat = 'sceneList'.
    """
    with open(in_file, 'r') as f:
        sr = yaml.safe_load(f)
    #results = sr['results']
    #entityIds = [r['entityId'] for r in results]
    output = {}
    output['datasetName'] = dataset_name
    output['products'] = prod_types
    #output['entityIds'] = entityIds
    output['entityIds'] = sr['results']
    #print(output)
    with open(out_file, 'w') as f:
        yaml.dump(output, f, default_flow_style=False)

def update_search_params(in_file, startDate=None, endDate=None):
    """
    Update the systematic search parameter file to use the most recent date, or the date 
    specified by startDate and endDate.
    """
    today = datetime.now().date()
    td = timedelta(days=1)
    yesterday = today - td
    with open(in_file, 'r') as f:
        data = yaml.safe_load(f)
    
    data['metadataUpdateFilter']['startDate'] = str(yesterday)
    data['metadataUpdateFilter']['endDate'] = str(today)
    
    with open(in_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

def download_files(in_file, out_dir, prod_types=None):
    """
    Read a YAML file with download URLs and download all that match prod_type filter.
    If prod_types is not provided, download all.
    """
    q = Queue(maxsize=0)
    urls = []
    with open(in_file, 'r') as f:
        logger.debug('Reading {}'.format(in_file))
        data = yaml.safe_load(f)
    for entity in data:
        url = entity['url']
        display_id = re.compile(DISPLAYID_RE).search(url).group()
        if entity['product'] == 'FR_BUND':
            file_name = '{}.zip'.format(display_id)
        elif entity['product'] == 'STANDARD':
            file_name = '{}.tar.gz'.format(display_id)
        # Check extensions for FR_REFL, FR_THERM, FR_QB and add cases.
        logger.debug('Adding entry to the download list. URL: {}, file name: {}'.format(url, file_name))
        urls.append({'url': url, 'file name': file_name})

    num_threads = min(MAX_DOWNLOADS, len(urls))
    logger.debug('Number of parallel downloads set to {}'.format(num_threads))
    results = [{} for x in urls]
    for i in range(len(urls)):
        logger.debug('Populating download queue with {}'.format(urls[i]))
        q.put((i, urls[i]))
    
    for i in range(num_threads):
        logger.debug('Starting thread {}'.format(i))
        worker = Thread(target=download_product, args=(q, results, out_dir))
        worker.setDaemon(True)
        worker.start()
    
    q.join()
    logger.debug(results)
    logger.info('All downloads processed')

def download_product(q, result, out_dir=None):
    """
    Threaded function for downloading products
    """
    while not q.empty():
        work = q.get()
        try:
            logger.info('Trying to download from {} to {}\\{}'.format(work[1]['url'], out_dir, work[1]['file name']))
            download(work[1]['url'], '{}/{}'.format(out_dir, work[1]['file name']))
            result[work[0]] = {'Status': 'Downloaded', 'URL': work[1]['url'], 'File Name': work[1]['file name']}
        except:
            logger.exception('Download failed! {}'.format(work[1]['url']))
            result[work[0]] = {'Status': 'Failed', 'URL': work[1]['url'], 'File Name': work[1]['file name']}
        q.task_done()
    return True

def download(url, local_file):
    """
    Download data from URL to local file as stream.
    [TODO] Currently uses a hacked-in temporary file name. Improve later by making it configurable.
    """
    tmp_local_file = "{}{}{}".format(TMP_PREFIX, local_file, TMP_SUFFIX)
    with requests.get(url, stream=True) as r:
        logger.debug('Opening download stream for {}'.format(url))
        with open(tmp_local_file, 'wb') as f:
            logger.debug('Starting to write to temp file {}'.format(tmp_local_file))
            shutil.copyfileobj(r.raw, f)
    logger.debug('Finished downloading {}'.format(url))
    logger.debug('Renaming temp file to {}'.format(local_file))
    os.rename(tmp_local_file, local_file)
    return local_file
