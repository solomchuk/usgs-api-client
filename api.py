"""
Implement the USGS Inventory API methods.
Note that HTTP POST is used for all API methods.
"""

import json
import logging
import logging.config
import os

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
import yaml

import payloads

abs_mod_dir = os.path.dirname(__file__)

with open(os.path.join(abs_mod_dir, 'logging.conf'), 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)


def _submit_request(url, payload):
    """
    POST a request to the USGS API server. The URL and payload are defined in
    the corresponding API method function.
    """
    logger.debug("API call URL: {}".format(url))
    if 'login' in url:
        logger.debug("API call payload hidden.")
    else:
        logger.debug("API call payload: {}".format(payload))
    
    try:
        r = requests.post(url, payload)
        r.raise_for_status()
    except HTTPError:
        logger.exception('Server responded with an HTTP error for {}!'.format(url))
    except ConnectionError:
        logger.exception('Error while trying to open {}!'.format(url))
    else:
        logger.debug("Received response:\n{}".format(json.dumps(r.json(), indent=4)))
        return r.json()   

def datasetfields(endpoint, apiKey, payload):
    """
    Get a list of fields available in the supplied dataset.
    Valid API key is required for this request - use login() to obtain.
    See params/datasetfields.yaml for the structure of the payload argument.
    The response contains a list of dataset field objects - see
    MetadataField() class in datamodels.py.
    """
    url = '{}/datasetfields'.format(endpoint)
    payload = {
        "jsonRequest": payloads.datasetfields(apiKey, **payload)
    }
    return _submit_request(url, payload)

def datasets(endpoint, apiKey, payload):
    """
    Get a list of datasets available to the user.
    Valid API key is required for this request - use login() to obtain.
    See params/datasets.yaml for the structure of payload argument.
    The response contains a list of dataset objects - see Dataset() class in datamodels.py.
    """
    url = '{}/datasets'.format(endpoint)
    payload = {
        "jsonRequest": payloads.datasets(apiKey, **payload)
    }
    return _submit_request(url, payload)

def grid2ll(endpoint, apiKey, payload):
    """
    Translate grid reference to coordinates.
    See params/grid2ll.yaml for the structure of payload argument.
    The response contains a list of coordinates defining the shape - see Coordinate() class in datamodels.py.
    apiKey parameter is not used but included for consistency with other functions.
    """
    url = '{}/grid2ll'.format(endpoint)
    payload = {
        "jsonRequest": payloads.grid2ll(**payload)
    }
    return _submit_request(url, payload)

def idlookup(endpoint, apiKey, payload):
    """
    Translate from one ID type to another: entityId <-> displayId.
    Valid API key is required for this request - use login() to obtain.
    See params/idlookup.yaml for the structure of payload argument.
    The response contains a dictionary of objects - keys are inputField values, values are the corresponding translations.
    """
    url = '{}/idlookup'.format(endpoint)
    payload = {
        "jsonRequest": payloads.idlookup(apiKey, **payload)
    }
    return _submit_request(url, payload)

def login(endpoint, payload):
    """
    Get an API key by providing valid username/password pair.
    See params/login.yaml for the structure of payload.
    The response contains a hexadecimal string ("data") which is the API key.
    """
    url = '{}/login'.format(endpoint)
    payload = {
        "jsonRequest": payloads.login(**payload)
    }
    return _submit_request(url, payload)

def logout(endpoint, apiKey):
    """
    Destroy the user's current API key to prevent it from being used in the future.
    The request only requires the API key to be provided.
    Successful logouts result in a response containing no error and "data": True.
    If the key was stored in a file locally, the file is removed.
    """
    url = '{}/logout'.format(endpoint)
    payload = {
        "jsonRequest": payloads.logout(apiKey)
    }
    return _submit_request(url, payload)

def notifications(endpoint, apiKey):
    """
    Get all system notifications for the current application context.
    Valid API key is required for this request - use login() to obtain.
    The response contains a list of notifications - see Notification() class in datamodels.py.
    """
    url = '{}/notifications'.format(endpoint)
    payload = {
        "jsonRequest": payloads.notifications(apiKey)
    }
    return _submit_request(url, payload)

def cleardownloads(endpoint, apiKey, payload=None):
    """
    Clear all pending donwloads from the user's download queue.
    Valid API key is required for this request - use login() to obtain.
    See params/cleardownloads.yaml for the structure of payload.
    The request does not have a response. Successful execution is assumed if no errors are thrown.
    """
    url = '{}/cleardownloads'.format(endpoint)
    if payload:
        payload = {
            "jsonRequest": payloads.cleardownloads(apiKey, **payload)
        }
    else:
        payload = {
            "jsonRequest": payloads.cleardownloads(apiKey)
        }
    return _submit_request(url, payload)

def deletionsearch(endpoint, apiKey, payload):
    """
    Detect deleted scenes in a dataset that supports it.
    Valid API key is required for this request - use login() to obtain.
    See params/deletionsearch.yaml for the structure of payload.
    The request returns a DeletionSearchResponse() object - see datamodels.py.
    """
    url = '{}/deletionsearch'.format(endpoint)
    payload = {
        "jsonRequest": payloads.deletionsearch(apiKey, **payload)
    }
    return _submit_request(url, payload)

def metadata(endpoint, apiKey, payload):
    """
    Find (metadata for) downloadable products for each dataset.
    If a download is marked as not available, an order must be placed to generate that product.
    Valid API key is required for this request - use login() to obtain.
    See params/metadata.yaml for the structure of payload.
    The request returns a list of SceneMetdata() objects - see datamodels.py.
    """
    url = '{}/metadata'.format(endpoint)
    payload = {
        "jsonRequest": payloads.metadata(apiKey, **payload)
    }
    return _submit_request(url, payload)

def search(endpoint, apiKey, payload):
    """
    Perform a product search using supplied criteria.
    Valid API key is required for this request - use login() to obtain.
    See params/search.yaml for the structure of payload.
    The request returns a SearchResponse() object - see datamodels.py.
    """
    url = '{}/search'.format(endpoint)
    payload = {
        "jsonRequest": payloads.search(apiKey, **payload)
    }
    return _submit_request(url, payload)

def hits(endpoint, apiKey, payload):
    """
    Determine the number of hits a search returns.
    Valid API key is required for this request - use login() to obtain.
    See params/hits.yaml for the structure of payload.
    The request returns an integer denoting the number of scenes the search matches.
    """
    url = '{}/hits'.format(endpoint)
    payload = {
        "jsonRequest": payloads.hits(apiKey, **payload)
    }
    return _submit_request(url, payload)

def status(endpoint):
    """
    Get the current status of the API endpoint.
    This method does not require any parameters.
    The response contains a status orject relfecting the current status of the called API - 
    see Status() class in datamodels.py.
    """
    url = '{}/status'.format(endpoint)
    payload = {
        "jsonRequest": payloads.status()
    }
    return _submit_request(url, payload)

def download(endpoint, apiKey, payload):
    """
    Get download URLs for the supplied list of entity IDs.
    Valid API key is required for this request - use login() to obtain.
    See params/download.yaml for the structure of payload.
    Returns a list of DownloadRecord() (or does it?) objects - see datamodels.py.
    """
    url = '{}/download'.format(endpoint)
    payload = {
        "jsonRequest": payloads.download(apiKey, **payload)
    }
    return _submit_request(url, payload)

def downloadoptions(endpoint, apiKey, payload):
    """
    Get download options for the supplied list of entity IDs.
    Valid API key is required for this request - use login() to obtain.
    See params/downloadoptions.yaml for the structure of payload.
    Returns a list of DownloadOption() objects - see datamodels.py.
    """
    url = '{}/downloadoptions'.format(endpoint)
    payload = {
        "jsonRequest": payloads.downloadoptions(apiKey, **payload)
    }
    return _submit_request(url, payload)

# Below this comment - service methods found in USGS example script
# Not implemented yet.

def getbulkdownloadproducts(endpoint, apiKey, payload):
    """
    NYI: Get Bulk Download Products.
    Request parameters:
     - API Key
     - Dataset Name
     - Entity IDs
    """
    raise NotImplementedError

def clearbulkdownloadorder(endpoint, apiKey, payload):
    """
    NYI: Clear Bulk Download Order.
    Request parameters:
     - API Key
     - Dataset Name (optional?)
    """
    raise NotImplementedError

def clearorder(endpoint, apiKey, payload):
    """
    NYI: Clear Order
    Request parameters:
     - API Key
     - Dataset Name (optional?)
    """
    raise NotImplementedError

def itembasket(endpoint, apiKey, payload):
    """
    NYI: Item Basket
    Request parameters:
     - API Key
    """
    raise NotImplementedError

def getorderproducts(endpoint, apiKey, payload):
    """
    NYI: Get Order Products
     - API Key
     - Dataset Name
     - Entity IDs
    """
    raise NotImplementedError

def submitbulkdownloadorder(endpoint, apiKey, payload):
    """
    NYI: Submit Bulk Download Order
     - API Key
    """
    raise NotImplementedError

def submitorder(endpoint, apiKey, payload):
    """
    NYI: Submit Order
     - API Key
    """
    raise NotImplementedError

def updatebulkdownloadscene(endpoint, apiKey, payload):
    """
    NYI: Update Bulk Download Scene
     - API Key
     - Dataset Name
     - Download Codes
     - Entity ID
    """
    raise NotImplementedError

def updateorderscene(endpoint, apiKey, payload):
    """
    NYI: Update Order Scene
     - API Key
     - Dataset Name
     - Product Code
     - Output Media
     - Option
     - Entity ID
    """
    raise NotImplementedError

def createsubscription(endpoint, apiKey, payload):
    """
    NYI: Create Subscription
     - ?
    """
    raise NotImplementedError

def downloadrequest(endpoint, apiKey, payload):
    """
    NYI: Download Order Request
     - API Key ?
     - Downloads
     - Data Paths
     - Configuration Code
     - Label
    """
    raise NotImplementedError

def downloadstatus(endpoint, apiKey, payload):
    """
    NYI: Download Status
     - API Key ?
     - Labels
     - Active Only
    """
    raise NotImplementedError

def downloadsummary(endpoint, apiKey, payload):
    """
    NYI: Download Summary
     - API Key ?
     - Labels
     - Send Email
    """
    raise NotImplementedError

def getdownloads(endpoint, apiKey, payload):
    """
    NYI: Get Downloads
     - API Key
     - Labels
     - Max Downloads
    """
    raise NotImplementedError

def loadordereddownloads(endpoint, apiKey, payload):
    """
    NYI: Load Ordered Downloads
     - API Key
     - Labels
    """
    raise NotImplementedError

def orderstatus(endpoint, apiKey, payload):
    """
    NYI: Order Status
     - API Key
     - Order Number
    """
    raise NotImplementedError
