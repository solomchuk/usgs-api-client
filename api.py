#!/usr/bin/env python

"""

"""

import os
from os.path import expanduser
import requests
import payloads
import datamodels
import json

# The USGS API endpoint
USGS_API_ENDPOINT = "https://earthexplorer.usgs.gov/inventory/json/v/1.4.1"
KEY_FILE = os.path.join(expanduser("~"), ".usgs_api_key")

class USGSError(Exception):
    pass

def _get_saved_key(apiKey):
    """
    """
    if apiKey is None and os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r', encoding='utf-8') as f:
            apiKey = f.read()
    return apiKey

def _catch_usgs_error(data):
    """
    Check the response object from USGS API for errors.
    Empty return if no error.
    Raise USGSError if something was wrong.
    """
    errorCode = data["errorCode"]
    if errorCode is None:
        return
    
    error = data["error"]
    raise USGSError('{}: {}'.format(errorCode, error))

def datasetfields(apiKey, datasetName):
    """
    Get a list of fields available in the supplied dataset.
    Valid API key is required for this request - use login() to obtain.
    See params/datasetfields.yaml for the structure of the payload argument.
    The response contains a list of dataset field objects - see MetadataField() class in datamodels.py.
    """
    url = '{}/datasetfields'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.datasetfields(apiKey, datasetName)
    }

    response = requests.post(url, payload).json()

    _catch_usgs_error(response)

    return json.dumps(response, indent=4)

def datasets(apiKey, payload):
    """
    Get a list of datasets available to the user.
    Valid API key is required for this request - use login() to obtain.
    See params/datasets.yaml for the structure of payload argument.
    The response contains a list of dataset objects - see Dataset() class in datamodels.py.
    """
    url = '{}/datasets'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.datasets(apiKey, **payload)
    }

    response = requests.post(url, payload).json()

    _catch_usgs_error(response)

    return json.dumps(response, indent=4)

def grid2ll(payload):
    """
    Translate grid reference to coordinates.
    See params/grid2ll.yaml for the structure of payload argument.
    The response contains a list of coordinates defining the shape - see Coordinate() class in datamodels.py.
    """

    url = '{}/grid2ll'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.grid2ll(**payload)
    }

    response = requests.post(url, payload).json()

    _catch_usgs_error(response)

    return json.dumps(response, indent=4)

def idlookup(apiKey, payload):
    """
    Translate from one ID type to another: entityId <-> displayId.
    Valid API key is required for this request - use login() to obtain.
    See params/idlookup.yaml for teh structure of payload argument.
    The response contains a dictionary of objects - keys are inputField values, values are the corresponding translations.
    """

    url = '{}/idlookup'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.idlookup(apiKey, **payload)
    }

    response = requests.post(url, payload).json()

    _catch_usgs_error(response)

    return json.dumps(response, indent=4)

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

    resp = requests.post(url,payload)
    if resp.status_code is not 200:
        raise USGSError(resp.text)
    response = resp.json()
    apiKey = response["data"]

    if apiKey is None:
        raise USGSError(response["error"])
    
    if store:
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

    response = requests.post(url,payload).json()

    _catch_usgs_error(response)

    if os.path.exists(KEY_FILE):
        os.remove(KEY_FILE)

    return response

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

    response = requests.post(url, payload).json()

    _catch_usgs_error(response)

    return response

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
    print(payload)
    try:
        requests.post(url, payload)
        print('Download queue cleared.')
    except USGSError as exc:
        print(exc)

def deletionsearch(apiKey, payload):
    """
    Detect deleted scenes in a dataset that supports it.
    Valid API key is required for this request - use login() to obtain.
    See params/deletionsearch.yaml for the structure of payload.
    The request returns a DeletionSearchResponse() object - see datamodels.py.
    """

    url = '{}/deletionsearch'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.deletionsearch(apiKey, **payload)
    }

    response = requests.post(url, payload).json()

    _catch_usgs_error(response)

    return json.dumps(response, indent=4)

def metadata(apiKey, payload):
    """
    Find (metadata for) downloadable products for each dataset.
    If a download is marked as not available, an order must be placed to generate that product.
    Valid API key is required for this request - use login() to obtain.
    See params/metadata.yaml for the structure of payload.
    The request returns a list of SceneMetdata() objects - see datamodels.py.
    """

    url = '{}/metadata'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.metadata(apiKey, **payload)
    }

    response = requests.post(url, payload).json()

    _catch_usgs_error(response)

    return json.dumps(response, indent=4)

def search(apiKey, payload):
    """
    Perform a product search using supplied criteria.
    Valid API key is required for this request - use login() to obtain.
    See params/search.yaml for the structure of payload.
    The request returns a SearchResponse() object - see datamodels.py.
    """
    
    url = '{}/metadata'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.search(apiKey, **payload)
    }

    response = requests.post(url, payload).json()

    _catch_usgs_error(response)

    return json.dumps(response, indent=4)

def hits(apiKey, payload):
    """
    Determine the number of hits a search returns.
    Valid API key is required for this request - use login() to obtain.
    See params/hits.yaml for the structure of payload.
    The request returns an integer denoting the number of scenes the search matches.
    """

    url = '{}/hits'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.hits(apiKey, **payload)
    }

    response = requests.post(url, payload).json()

    _catch_usgs_error(response)

    return json.dumps(response, indent=4)

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

    response = requests.post(url, payload).json()

    _catch_usgs_error(response)

    return response

def download(apiKey, payload):
    """
    Get download URLs for the supplied list of entity IDs.
    Valid API key is required for this request - use login() to obtain.
    See params/download.yaml for the structure of payload.
    Returns a list of DownloadRecord() (or does it?) objects - see datamodels.py.
    """

    url = '{}/download'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.download(apiKey, **payload)
    }

    response = requests.post(url, payload).json()
    _catch_usgs_error(response)

    return json.dumps(response, indent=4)

def downloadoptions(apiKey, payload):
    """
    Get download options for the supplied list of entity IDs.
    Valid API key is required for this request - use login() to obtain.
    See params/downloadoptions.yaml for the structure of payload.
    Returns a list of DownloadOption() objects - see datamodels.py.
    """

    url = '{}/downloadoptions'.format(USGS_API_ENDPOINT)
    payload = {
        "jsonRequest": payloads.downloadoptions(apiKey, **payload)
    }

    response = requests.post(url, payload).json()

    _catch_usgs_error(response)

    return json.dumps(response, indent=4)
