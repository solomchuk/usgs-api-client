#!/usr/bin/env python

"""

"""

import json
import logging
import logging.config
import os
from os.path import expanduser

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
import yaml

import datamodels
import payloads
import usgs_exceptions as usgs_exp

# The USGS API endpoint
USGS_API_ENDPOINT = "https://earthexplorer.usgs.gov/inventory/json/v/1.4.1"
KEY_FILE = os.path.join(expanduser("~"), ".usgs_api_key")
abs_mod_dir = os.path.dirname(__file__)

with open(os.path.join(abs_mod_dir, 'logging.conf'), 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger(__name__)

class USGSError(Exception):
    """
    Raise a generic USGS error.
    See https://earthexplorer.usgs.gov/inventory/documentation/errors
    for possible response codes and messages.
    """

def _get_saved_key(apiKey):
    """
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        logger.debug("Getting API key from file {}".format(KEY_FILE))
        with open(KEY_FILE, 'r', encoding='utf-8') as f:
            apiKey = f.read()
    return apiKey

def _catch_usgs_error(response):
    """
    Check the response object from USGS API for errors.
    Empty return if no error.
    Raise USGSError if something was wrong.
    TODO: Figure out how to integrate this with logging.
    """
    errorCode = response["errorCode"]
    if errorCode is None:
        return
    
    error = response["error"]
    # TODO Hack to force re-authorisation if API key is invalid
    if errorCode == 'AUTH_UNAUTHORIZED':
        raise usgs_exp.AuthUnauthorizedError('{}: {}'.format(errorCode, error))
        # TODO add a login() call with default login.yaml param file
    else:
        raise USGSError('{}: {}'.format(errorCode, error))

def _submit_request(url, payload):
    """
    POST a request to the USGS API server. The URL and payload are defined in
    the corresponding API method function.
    """
    logger.debug("API call URL: {}".format(url))
    logger.debug("API call payload: {}".format(payload))
    try:
        r = requests.post(url, payload)
        r.raise_for_status()
    except HTTPError:
        logger.exception('Server responded with an HTTP error for {}!'.format(url))
    except ConnectionError:
        logger.exception('Error while trying to open {}!'.format(url))
    else:
        response = r.json()
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        _catch_usgs_error(response)
        return response   

def datasetfields(apiKey, payload):
    """
    Get a list of fields available in the supplied dataset.
    Valid API key is required for this request - use login() to obtain.
    See params/datasetfields.yaml for the structure of the payload argument.
    The response contains a list of dataset field objects - see
    MetadataField() class in datamodels.py.
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        apiKey = _get_saved_key(apiKey)
    url = '{}/datasetfields'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.datasetfields(apiKey, **payload)
    }
    
    return _submit_request(url, payload)

def datasets(apiKey, payload):
    """
    Get a list of datasets available to the user.
    Valid API key is required for this request - use login() to obtain.
    See params/datasets.yaml for the structure of payload argument.
    The response contains a list of dataset objects - see Dataset() class in datamodels.py.
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        apiKey = _get_saved_key(apiKey)
    url = '{}/datasets'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.datasets(apiKey, **payload)
    }
    
    return _submit_request(url, payload)

def grid2ll(apiKey, payload):
    """
    Translate grid reference to coordinates.
    See params/grid2ll.yaml for the structure of payload argument.
    The response contains a list of coordinates defining the shape - see Coordinate() class in datamodels.py.
    apiKey parameter is not used but included for consistency with other functions.
    """

    url = '{}/grid2ll'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.grid2ll(**payload)
    }

    return _submit_request(url, payload)

def idlookup(apiKey, payload):
    """
    Translate from one ID type to another: entityId <-> displayId.
    Valid API key is required for this request - use login() to obtain.
    See params/idlookup.yaml for the structure of payload argument.
    The response contains a dictionary of objects - keys are inputField values, values are the corresponding translations.
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        apiKey = _get_saved_key(apiKey)
    
    url = '{}/idlookup'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.idlookup(apiKey, **payload)
    }

    return _submit_request(url, payload)

def login(username, password, store=True):
    """
    Get an API key by providing valid username/password pair.
    See params/login.yaml for the structure of payload.
    The response contains a hexadecimal string ("data") which is the API key.
    """
    url = '{}/login'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.login(username, password)
    }
    logger.debug("API call URL: {}".format(url))
    logger.debug("API call payload hidden.")
    resp = requests.post(url,payload)
    if resp.status_code is not 200:
        raise USGSError(resp.text)
    response = resp.json()
    logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
    apiKey = response["data"]

    if apiKey is None:
        raise USGSError(response["error"])
    
    if store:
        logger.debug("Writing API key to file {}".format(KEY_FILE))
        with open(KEY_FILE, "w") as f:
            f.write(apiKey)
        
    return response

def logout(apiKey=None):
    """
    Destroy the user's current API key to prevent it from being used in the future.
    The request only requires the API key to be provided.
    Successful logouts result in a response containing no error and "data": True.
    If the key was stored in a file locally, the file is removed.
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        apiKey = _get_saved_key(apiKey)
    
    url = '{}/logout'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.logout(apiKey)
    }

    if os.path.exists(KEY_FILE):
        logger.debug("Removing API key file {}".format(KEY_FILE))
        os.remove(KEY_FILE)

    return _submit_request(url, payload)

def notifications(apiKey):
    """
    Get all system notifications for the current application context.
    Valid API key is required for this request - use login() to obtain.
    The response contains a list of notifications - see Notification() class in datamodels.py.
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        apiKey = _get_saved_key(apiKey)
    url = '{}/notifications'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.notifications(apiKey)
    }

    return _submit_request(url, payload)

def cleardownloads(apiKey, payload=None):
    """
    Clear all pending donwloads from the user's download queue.
    Valid API key is required for this request - use login() to obtain.
    See params/cleardownloads.yaml for the structure of payload.
    The request does not have a response. Successful execution is assumed if no errors are thrown.
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        apiKey = _get_saved_key(apiKey)
    url = '{}/cleardownloads'.format(USGS_API_ENDPOINT)
    if payload:
        payload = {
            "jsonRequest": payloads.cleardownloads(apiKey, payload)
        }
    else:
        payload = {
            "jsonRequest": payloads.cleardownloads(apiKey)
        }
    logger.debug("API call URL: {}".format(url))
    logger.debug("API call payload: {}".format(payload))
    try:
        requests.post(url, payload)
        logger.debug('Download queue cleared.')
    except USGSError as exc:
        logger.exception(exc)
        raise

def deletionsearch(apiKey, payload):
    """
    Detect deleted scenes in a dataset that supports it.
    Valid API key is required for this request - use login() to obtain.
    See params/deletionsearch.yaml for the structure of payload.
    The request returns a DeletionSearchResponse() object - see datamodels.py.
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        apiKey = _get_saved_key(apiKey)
    url = '{}/deletionsearch'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.deletionsearch(apiKey, **payload)
    }

    return _submit_request(url, payload)

def metadata(apiKey, payload):
    """
    Find (metadata for) downloadable products for each dataset.
    If a download is marked as not available, an order must be placed to generate that product.
    Valid API key is required for this request - use login() to obtain.
    See params/metadata.yaml for the structure of payload.
    The request returns a list of SceneMetdata() objects - see datamodels.py.
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        apiKey = _get_saved_key(apiKey)
    url = '{}/metadata'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.metadata(apiKey, **payload)
    }

    return _submit_request(url, payload)

def search(apiKey, payload):
    """
    Perform a product search using supplied criteria.
    Valid API key is required for this request - use login() to obtain.
    See params/search.yaml for the structure of payload.
    The request returns a SearchResponse() object - see datamodels.py.
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        apiKey = _get_saved_key(apiKey)
    url = '{}/search'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.search(apiKey, **payload)
    }

    return _submit_request(url, payload)

def hits(apiKey, payload):
    """
    Determine the number of hits a search returns.
    Valid API key is required for this request - use login() to obtain.
    See params/hits.yaml for the structure of payload.
    The request returns an integer denoting the number of scenes the search matches.
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        apiKey = _get_saved_key(apiKey)
    url = '{}/hits'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.hits(apiKey, **payload)
    }

    return _submit_request(url, payload)

def status():
    """
    Get the current status of the API endpoint.
    This method does not require any parameters.
    The response contains a status orject relfecting the current status of the called API - 
    see Status() class in datamodels.py.
    """

    url = '{}/status'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.status()
    }

    return _submit_request(url, payload)

def download(apiKey, payload):
    """
    Get download URLs for the supplied list of entity IDs.
    Valid API key is required for this request - use login() to obtain.
    See params/download.yaml for the structure of payload.
    Returns a list of DownloadRecord() (or does it?) objects - see datamodels.py.
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        apiKey = _get_saved_key(apiKey)
    url = '{}/download'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.download(apiKey, **payload)
    }

    return _submit_request(url, payload)

def downloadoptions(apiKey, payload):
    """
    Get download options for the supplied list of entity IDs.
    Valid API key is required for this request - use login() to obtain.
    See params/downloadoptions.yaml for the structure of payload.
    Returns a list of DownloadOption() objects - see datamodels.py.
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        apiKey = _get_saved_key(apiKey)
    url = '{}/downloadoptions'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.downloadoptions(apiKey, **payload)
    }

    return _submit_request(url, payload)
