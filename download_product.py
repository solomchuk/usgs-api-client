#!/usr/bin/env python

"""
Login to USGS Inventory API server
[Optional] Save api key to file
Obtain download URL for the specified scene
Download the specified scene to the target directory
[Optional] Logout
"""

import argparse
import logging
import logging.config
import os
import re
import shutil
from os.path import expanduser
from queue import Queue
from threading import Thread

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
import yaml

import api
import payloads

DISPLAYID_RE = r'L[COT]\d{2}_(L1GT|L1GS|L1TP)_\d{6}_\d{8}_\d{8}_\d{2}_(RT|T1|T2)'
MAX_DOWNLOADS = 10
TMP_PREFIX = "."
TMP_SUFFIX = "_lock"
KEY_FILE = os.path.join(expanduser("~"), ".usgs_api_key")
abs_mod_dir = os.path.dirname(__file__)

with open(os.path.join(abs_mod_dir, 'logging.conf'), 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)

def get_saved_key():
    """
    Try to get the API key from a saved file.
    """
    logger.debug("Getting API key from file {}".format(KEY_FILE))
    with open(KEY_FILE, 'r', encoding='utf-8') as f:
        apiKey = f.read()
    if apiKey:
        logger.debug('Found API key in file, will try to reuse')
        return apiKey

def check_key_validity(endpoint, apiKey):
    """
    Perform a USGS API notifications query to check if API key is still valid
    """
    response = api.notifications(endpoint, apiKey)
    errorCode = response['errorCode']
    error = response['error']
    if errorCode is None:
        logger.info('API Key {} appears to be valid, will try to reuse'.format(apiKey))
        return True
    elif errorCode == 'AUTH_UNAUTHORIZED':
        logger.warn('API Key {} appears to be invalid, new login required'.format(apiKey))
        return False
    else:
        logger.error('Error encountered: {} - {}'.format(errorCode, error))
        return False

def login(endpoint, cred_file, store):
    """
    Perform USGS Inventory API authentication
    """
    with open(cred_file, 'r') as f:
        payload = yaml.safe_load(f)
    response = api.login(endpoint, payload)
    errorCode = response['errorCode']
    error = response['error']
    if errorCode is None:
        if store:
            logger.debug("Writing API key to file {}".format(KEY_FILE))
            with open(KEY_FILE, "w") as f:
                f.write(response['data'])
        return response['data']
    else:
        logger.error('Authentication error: {} - {}'.format(errorCode, error))
        exit('Can\'t continue without successful authentication, exiting')

def get_url(endpoint, apiKey, payload):
    """
    Obtain download URL(s) for desired product(s)
    """
    return api.download(endpoint, apiKey, payload)

def download_files(data, out_dir, prod_types=None):
    """
    Read a YAML file with download URLs and download all that match prod_type filter.
    If prod_types is not provided, download all.
    """
    q = Queue(maxsize=0)
    urls = []
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
            download(work[1]['url'], out_dir, work[1]['file name'])
            result[work[0]] = {'Status': 'Downloaded', 'URL': work[1]['url'], 'File Name': work[1]['file name']}
        except:
            logger.exception('Download failed! {}'.format(work[1]['url']))
            result[work[0]] = {'Status': 'Failed', 'URL': work[1]['url'], 'File Name': work[1]['file name']}
        q.task_done()
    return True

def download(url, out_dir, local_file):
    """
    Download data from URL to local file as stream.
    """
    tmp_local_file = '{}{}{}'.format(TMP_PREFIX, local_file, TMP_SUFFIX)
    tmp_local_fullpath = os.path.join(os.sep, out_dir + os.sep, tmp_local_file)
    final_local_fullpath = os.path.join(os.sep, out_dir + os.sep, local_file)
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
    except HTTPError:
        logger.exception('Server responded with an HTTP error for {}!'.format(url))
    except ConnectionError:
        logger.exception('Error while trying to open {}!'.format(url))
    else:
        try:
            with r:
                logger.debug('Opening download stream for {}'.format(url))
                with open(tmp_local_fullpath, 'wb') as f:
                    logger.debug('Starting to write to temp file {}'.format(tmp_local_fullpath))
                    shutil.copyfileobj(r.raw, f)
            logger.debug('Finished downloading {}'.format(url))
            logger.debug('Renaming temp file to {}'.format(final_local_fullpath))
            os.rename(tmp_local_fullpath, final_local_fullpath)
            return final_local_fullpath
        except Timeout:
            logger.exception('Request timed out: {}'.format(url))

def logout(endpoint, apiKey):
    """
    Perform USGS Inventory API logout
    """
    return api.logout(endpoint, apiKey)

def main():
    """
    Login to the USGS Inventory API service (or reuse an existing key).
    Request the download URL for the specified product.
    Download the product to the target directory.
    """
    arg_parser = argparse.ArgumentParser(description='Download the specified Landsat 8 product')
    arg_parser.add_argument('-c', '--credentialFile', help='API credential file', required=True)
    arg_parser.add_argument('-d', '--datasetName', help='Dataset Name', required=True)
    arg_parser.add_argument('-i', '--entityIds', nargs='*', help='Product entity IDs', required=True)
    arg_parser.add_argument('-p', '--products', nargs='*', help='Product types to download', required=True)
    arg_parser.add_argument('-s', '--saveKey', action='store_true', help='Save API key after login', required=False)
    arg_parser.add_argument('-e', '--endpoint', help='API endpoint', required=True)
    arg_parser.add_argument('-f', '--directory', help='Downloads directory', required=True)
    args = arg_parser.parse_args()

    try:
        os.path.isfile(args.credentialFile)
    except FileNotFoundError:
        logger.exception('Credential file not found: {}'.format(args.credentialFile))
        exit('Can\'t continue without a credential file, exiting')

    try:
        os.path.isdir(args.directory)
    except IOError:
        logger.exception('Downloads directory not found: {}'.format(args.directory))
        exit('Can\'t continue without a valid target directory, exiting')

    if not os.path.isfile(KEY_FILE):
        logger.info('No key file found, performing new login')
        apiKey = login(args.endpoint, args.credentialFile, args.saveKey)
    else:
        apiKey = get_saved_key()
        if not check_key_validity(args.endpoint, apiKey):
            apiKey = login(args.endpoint, args.credentialFile, args.saveKey)

    download_payload = {
        'datasetName': args.datasetName,
        'products': args.products,
        'entityIds': args.entityIds
    }

    download_response = get_url(args.endpoint, apiKey, download_payload)
    errorCode = download_response['errorCode']
    error = download_response['error']
    if errorCode is None:
        data = download_response['data']
    else:
        logger.error('USGS error: {} - {}'.format(errorCode, error))
        exit()
    
    download_files(data, args.directory, args.products)

    if not args.saveKey:
        logger.info('Logging out to invalidate the API key {}'.format(apiKey))
        logout(args.endpoint, apiKey)
        if os.path.exists(KEY_FILE):
            logger.debug("Removing API key file {}".format(KEY_FILE))
            os.remove(KEY_FILE)

if __name__ == '__main__':
    main()