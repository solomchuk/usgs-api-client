#!/usr/bin/env python

"""
Login to USGS Inventory API server
[Optional] Save api key to file
Perform systematic search with supplied parameters
[Temp] List returned scenes
[Future] Create .properties files for each scene's download job
[Optional] Logout
"""

import argparse
import logging
import logging.config
import os
from os.path import expanduser

import yaml

import api
import payloads

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

def logout(endpoint, apiKey):
    """
    Perform USGS Inventory API logout
    """
    return api.logout(endpoint, apiKey)

def search(endpoint, apiKey, conf_file):
    """
    Perform USGS Inventory API search
    """
    with open(conf_file, 'r') as f:
        payload = yaml.safe_load(f)
    return api.search(endpoint, apiKey, payload)

def main():
    """
    Login to the USGS Inventory API service (or reuse an existing key).
    Perform a search request using parameters from a configuration file.

    """
    arg_parser = argparse.ArgumentParser(description='Daily systematic search script for Landsat 8 products')
    arg_parser.add_argument('-c', '--credentialFile', help='API credential file', required=True)
    arg_parser.add_argument('-o', '--configurationFile', help='API request configuration file', required=True)
    arg_parser.add_argument('-s', '--saveKey', action='store_true', help='Save API key after login', required=False)
    arg_parser.add_argument('-e', '--endpoint', help='API endpoint', required=True)
    args = arg_parser.parse_args()

    try:
        os.path.isfile(args.configurationFile)
    except FileNotFoundError:
        logger.exception('Configuration file not found: {}'.format(args.configurationFile))
        exit('Can\'t continue without a configuration file, exiting')

    try:
        os.path.isfile(args.credentialFile)
    except FileNotFoundError:
        logger.exception('Credential file not found: {}'.format(args.credentialFile))
        exit('Can\'t continue without a credential file, exiting')

    if not os.path.isfile(KEY_FILE):
        logger.info('No key file found, performing new login')
        apiKey = login(args.endpoint, args.credentialFile, args.saveKey)
    else:
        apiKey = get_saved_key()
        if not check_key_validity(args.endpoint, apiKey):
            apiKey = login(args.endpoint, args.credentialFile, args.saveKey)

    search_response = search(args.endpoint, apiKey, args.configurationFile)
    errorCode = search_response['errorCode']
    error = search_response['error']
    if errorCode is None:
        data = search_response['data']
    else:
        logger.error('Search error: {} - {}'.format(errorCode, error))
        exit()
    
    # For each entityId in data['results'], create a new .properties file

    if not args.saveKey:
        logger.info('Logging out to invalidate the API key {}'.format(apiKey))
        logout(args.endpoint, apiKey)
        if os.path.exists(KEY_FILE):
            logger.debug("Removing API key file {}".format(KEY_FILE))
            os.remove(KEY_FILE)


if __name__ == '__main__':
    main()