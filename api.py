#!/usr/bin/env python

"""

"""

import json
import logging
import logging.config
import os
from os.path import expanduser
from datetime import datetime as dt

import requests
import yaml

# Determine whether datamodels is actually needed
import datamodels
import payloads

# The USGS API endpoint
#USGS_API_ENDPOINT = "https://earthexplorer.usgs.gov/inventory/json/v/1.4.1"
#API_URL_STABLE = "https://m2m.cr.usgs.gov/api/api/json/stable"
#KEY_FILE = os.path.join(expanduser("~"), ".usgs_api_key")
abs_mod_dir = os.path.dirname(__file__)

with open(os.path.join(abs_mod_dir, 'logging.conf'), 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger(__name__)

class USGSError(Exception):
    pass

class ApiHandler(object):
    """
    1.5.0 TODO:
        Handler class
            Authn via X-Auth-Token header
            ✅Datetime for last API Key usage (invalidate key after 2 hours idle)
            ✅Optionally - set proxy headers
            Request params:
                ✅API method
                ✅payload
            ✅Response object
                Getters for response params
            Handler __str__ and __repr__ methods
        API methods
            Refactor existing methods to use handler
            Align the list of methods with 1.5.0, remove deprecated
        Data types/models
            Decide if will use (with getters?)
        Refactor logging
        ✅Remove API key file handling (move functionality to client)
        Remove default API endpoint definition?
        ?Make class params immutable?
    """

    def __init__(self, endpoint: str, apiKey=None, proxies=None):
        """
        Constructor for the API handler class. Endpoint URL is the only mandatory argument.
        TODO: add a check on URL validity.
        """
        self.endpoint = endpoint

        if apiKey is None:
            apiKey = ""
        self.apiKey = apiKey

        self.lastApiKeyUseTime = None

        if proxies is None:
            proxies = {}
        self.proxies = proxies

        self.lastApiMethod = ""
        self.lastRequestPayload = ""
        self.lastResponse = None
        super().__init__()

    def _catch_usgs_error(self, data):
        """
        Check the response object from USGS API for errors.
        Empty return if no error.
        Raise USGSError if something was wrong.
        TODO: Figure out how to integrate this with logging.
        """
        errorCode = data["errorCode"]
        if errorCode is None:
            return
        
        error = data["error"]
        raise USGSError('{}: {}'.format(errorCode, error))

    def login(self, username, password, userContext=None):
        """✅
        Get an API key by providing valid username/password pair.
        See params/login.yaml for the structure of payload.
        The response contains a hexadecimal string ("data") which is the API key.
        """
        url = "{}/login".format(self.endpoint)
        payload = payloads.login(username, password, userContext)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload hidden.")
        response = requests.post(url=url,json=payload,proxies=self.proxies)
        if response.status_code is not 200:
            raise USGSError(response.text)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())

        self.lastApiMethod = "login"
        # Hide user/pass
        self.lastRequestPayload = {"username":"hidden","password":"hidden"}
        self.lastResponse = response

        if response.json()["data"] is None:
            raise USGSError(response["error"])
        else:
            self.apiKey = response.json()["data"]
        self.lastApiKeyUseTime = dt.utcnow()

    def logout(self):
        """✅
        Destroy the user's current API key to prevent it from being used in the future.
        This request does not use request parameters and does not return a data value.
        Successful logouts result in a response containing no error and "data": True.
        """
        
        url = "{}/logout".format(self.endpoint)
        payload = payloads.logout()
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url,json=payload,headers=headers,proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())

        self.lastApiMethod = "logout"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.apiKey = ""
        self.lastApiKeyUseTime = None

    def notifications(self, systemId: str):
        """✅
        Get a notification list.
        The response contains a list of notifications - see Notification() class in datamodels.py.
        """

        url = "{}/notifications".format(self.endpoint)
        payload = payloads.notifications(systemId)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "notifications"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def data_owner(self, dataOwner: str):
        """✅
        This method is used to provide the contact information of the data owner.
        """
        url = "{}/data-owner".format(self.endpoint)
        payload = payloads.data_owner(dataOwner)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "data-owner"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def dataset(self, datasetId=None, datasetName=None):
        """✅
        This method is used to retrieve the dataset by id or name.
        """
        url = "{}/dataset".format(self.endpoint)
        payload = payloads.dataset(datasetId, datasetName)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "dataset"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def dataset_categories(self, catalog=None, includeMessages=None, publicOnly=None,
                            parentId=None, datasetFilter=None):
        """✅
        This method is used to search datasets under the categories.
        """
        url = "{}/dataset-categories".format(self.endpoint)
        payload = payloads.dataset_categories(catalog, includeMessages, publicOnly,
                                                parentId, datasetFilter)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "dataset-categories"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def dataset_coverage(self, datasetName: str):
        """✅
        Returns coverage for a given dataset.
        """
        url = "{}/dataset-coverage".format(self.endpoint)
        payload = payloads.dataset_coverage(datasetName)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "dataset-coverage"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def dataset_filters(self, datasetName: str):
        """✅
        This request is used to return the metadata filter fields for the specified dataset.
        These values can be used as additional criteria when submitting search and hit queries.
        """
        url = "{}/dataset-filters".format(self.endpoint)
        payload = payloads.dataset_filters(datasetName)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "dataset-filters"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def dataset_messages(self, catalog=None, datasetName=None, datasetNames=None):
        """✅
        Returns any notices regarding the given datasets features.
        """
        url = "{}/dataset-messages".format(self.endpoint)
        payload = payloads.dataset_messages(catalog, datasetName, datasetNames)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "dataset-messages"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def dataset_search(self, catalog=None, categoryId=None, datasetName=None, includeMessages=None,
                    publicOnly=None, includeUnknownSpatial=None, temporalFilter=None, spatialFilter=None):
        """✅
        This method is used to find datasets available for searching. By passing only API Key,
        all available datasets are returned. Additional parameters such as temporal range and spatial
        bounding box can be used to find datasets that provide more specific data. The dataset name
        parameter can be used to limit the results based on matching the supplied value against the public
        dataset name with assumed wildcards at the beginning and end.
        """
        url = "{}/dataset-search".format(self.endpoint)
        payload = payloads.dataset_search(catalog, categoryId, datasetName, includeMessages, publicOnly,
                                         includeUnknownSpatial, temporalFilter, spatialFilter)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "dataset-search"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def datasetfields(self, apiKey, datasetName):
        """
        🔲TODO: rename to "dataset-filters"

        Get a list of fields available in the supplied dataset.
        Valid API key is required for this request - use login() to obtain.
        See params/datasetfields.yaml for the structure of the payload argument.
        The response contains a list of dataset field objects - see MetadataField() class in datamodels.py.
        """
        if apiKey is None and os.path.exists(KEY_FILE):
            apiKey = self._get_saved_key(apiKey)
        url = '{}/datasetfields'.format(USGS_API_ENDPOINT)
        payload = {
            "jsonRequest": payloads.datasetfields(apiKey, datasetName)
        }
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        response = requests.post(url, payload).json()
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        self._catch_usgs_error(response)

        return response

    def datasets(self, apiKey, payload):
        """
        🔲TODO: rename to "dataset-search"

        Get a list of datasets available to the user.
        Valid API key is required for this request - use login() to obtain.
        See params/datasets.yaml for the structure of payload argument.
        The response contains a list of dataset objects - see Dataset() class in datamodels.py.
        """
        if apiKey is None and os.path.exists(KEY_FILE):
            apiKey = self._get_saved_key(apiKey)
        url = '{}/datasets'.format(USGS_API_ENDPOINT)
        payload = {
            "jsonRequest": payloads.datasets(apiKey, **payload)
        }
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        response = requests.post(url, payload).json()
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        self._catch_usgs_error(response)

        return response

    def grid2ll(self, apiKey, payload):
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
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        response = requests.post(url, payload).json()
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        self._catch_usgs_error(response)

        return response

    def idlookup(self, apiKey, payload):
        """
        🔲TODO: method removed. Functionality provided by "scene-list-add" + "scene-list-get"

        Translate from one ID type to another: entityId <-> displayId.
        Valid API key is required for this request - use login() to obtain.
        See params/idlookup.yaml for the structure of payload argument.
        The response contains a dictionary of objects - keys are inputField values, values are the corresponding translations.
        """
        if apiKey is None and os.path.exists(KEY_FILE):
            apiKey = self._get_saved_key(apiKey)
        
        url = '{}/idlookup'.format(USGS_API_ENDPOINT)
        payload = {
            "jsonRequest": payloads.idlookup(apiKey, **payload)
        }
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        response = requests.post(url, payload).json()
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        self._catch_usgs_error(response)

        return response


    def cleardownloads(self, apiKey, payload=None):
        """
        🔲TODO: method removed.

        Clear all pending donwloads from the user's download queue.
        Valid API key is required for this request - use login() to obtain.
        See params/cleardownloads.yaml for the structure of payload.
        The request does not have a response. Successful execution is assumed if no errors are thrown.
        """
        if apiKey is None and os.path.exists(KEY_FILE):
            apiKey = self._get_saved_key(apiKey)
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

    def deletionsearch(self, apiKey, payload):
        """
        🔲TODO: rename to "scene-search-delete"

        Detect deleted scenes in a dataset that supports it.
        Valid API key is required for this request - use login() to obtain.
        See params/deletionsearch.yaml for the structure of payload.
        The request returns a DeletionSearchResponse() object - see datamodels.py.
        """
        if apiKey is None and os.path.exists(KEY_FILE):
            apiKey = self._get_saved_key(apiKey)
        url = '{}/deletionsearch'.format(USGS_API_ENDPOINT)
        payload = {
            "jsonRequest": payloads.deletionsearch(apiKey, **payload)
        }
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        response = requests.post(url, payload).json()
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        self._catch_usgs_error(response)

        return response

    def metadata(self, apiKey, payload):
        """
        🔲TODO: rename to "scene-metadata"

        Find (metadata for) downloadable products for each dataset.
        If a download is marked as not available, an order must be placed to generate that product.
        Valid API key is required for this request - use login() to obtain.
        See params/metadata.yaml for the structure of payload.
        The request returns a list of SceneMetdata() objects - see datamodels.py.
        """
        if apiKey is None and os.path.exists(KEY_FILE):
            apiKey = self._get_saved_key(apiKey)
        url = '{}/metadata'.format(USGS_API_ENDPOINT)
        payload = {
            "jsonRequest": payloads.metadata(apiKey, **payload)
        }
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        response = requests.post(url, payload).json()
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        self._catch_usgs_error(response)

        return response

    def search(self, apiKey, payload):
        """
        🔲TODO: rename to "scene-search"

        Perform a product search using supplied criteria.
        Valid API key is required for this request - use login() to obtain.
        See params/search.yaml for the structure of payload.
        The request returns a SearchResponse() object - see datamodels.py.
        """
        if apiKey is None and os.path.exists(KEY_FILE):
            apiKey = self._get_saved_key(apiKey)
        url = '{}/search'.format(USGS_API_ENDPOINT)
        payload = {
            "jsonRequest": payloads.search(apiKey, **payload)
        }
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        response = requests.post(url, payload).json()
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        self._catch_usgs_error(response)

        return response

    def hits(self, apiKey, payload):
        """
        🔲TODO: method removed

        Determine the number of hits a search returns.
        Valid API key is required for this request - use login() to obtain.
        See params/hits.yaml for the structure of payload.
        The request returns an integer denoting the number of scenes the search matches.
        """
        if apiKey is None and os.path.exists(KEY_FILE):
            apiKey = self._get_saved_key(apiKey)
        url = '{}/hits'.format(USGS_API_ENDPOINT)
        payload = {
            "jsonRequest": payloads.hits(apiKey, **payload)
        }
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        response = requests.post(url, payload).json()
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        self._catch_usgs_error(response)

        return response

    def status(self):
        """
        🔲TODO: method removed
        
        Get the current status of the API endpoint.
        This method does not require any parameters.
        The response contains a status orject relfecting the current status of the called API - 
        see Status() class in datamodels.py.
        """

        url = '{}/status'.format(USGS_API_ENDPOINT)
        payload = {
            "jsonRequest": payloads.status()
        }
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        response = requests.post(url=url, json=payload, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "status"
        self.lastRequestPayload = payload
        self.lastResponse = response

        return response.json()

    def download(self, apiKey, payload):
        """
        Get download URLs for the supplied list of entity IDs.
        Valid API key is required for this request - use login() to obtain.
        See params/download.yaml for the structure of payload.
        Returns a list of DownloadRecord() (or does it?) objects - see datamodels.py.
        """
        if apiKey is None and os.path.exists(KEY_FILE):
            apiKey = self._get_saved_key(apiKey)
        url = '{}/download'.format(USGS_API_ENDPOINT)
        payload = {
            "jsonRequest": payloads.download(apiKey, **payload)
        }
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        response = requests.post(url, payload).json()
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        self._catch_usgs_error(response)

        return response

    def downloadoptions(self, apiKey, payload):
        """
        Get download options for the supplied list of entity IDs.
        Valid API key is required for this request - use login() to obtain.
        See params/downloadoptions.yaml for the structure of payload.
        Returns a list of DownloadOption() objects - see datamodels.py.
        """
        if apiKey is None and os.path.exists(KEY_FILE):
            apiKey = self._get_saved_key(apiKey)
        url = '{}/downloadoptions'.format(USGS_API_ENDPOINT)
        payload = {
            "jsonRequest": payloads.downloadoptions(apiKey, **payload)
        }
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        response = requests.post(url, payload).json()
        logger.debug("Received response:\n{}".format(json.dumps(response, indent=4)))
        self._catch_usgs_error(response)

        return response

    """
    def dataset-search():
        pass

    def download-labels():
        pass

    def download-order-load():
        pass

    def download-order-remove():
        pass

    def download-remove():
        pass

    def download-retrieve():
        pass

    def download-search():
        pass

    def grid2ll():
        pass

    def permissions():
        pass

    def scene-list-add():
        pass

    def scene-list-get():
        pass

    def scene-list-remove():
        pass

    def scene-list-summary():
        pass

    def scene-list-types():
        pass

    def scene-metadata():
        pass

    def scene-metadata-list():
        pass

    def scene-metadata-xml():
        pass

    def scene-search():
        pass

    def scene-search-delete():
        pass

    def scene-search-secondary():
        pass

    """