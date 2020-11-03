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

    def download_labels(self, downloadApplication=None):
        """
        Gets a list of unique download labels associated with the orders.
        """
        url = "{}/download-labels".format(self.endpoint)
        payload = payloads.download_labels(downloadApplication)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "download-labels"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def download_order_load(self, downloadApplication=none, label=None):
        """
        This method is used to prepare a download order for processing by moving the scenes
        into the queue for processing.
        """
        url = "{}/download-order-load".format(self.endpoint)
        payload = payloads.download_order_load(downloadApplication, label)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "download-order-load"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()
    
    def download_order_remove(self, label: str, downloadApplication=None):
        """
        This method is used to remove an order from the download queue.
        """
        url = "{}/download-order-remove".format(self.endpoint)
        payload = payloads.download_order_remove(label, downloadApplication)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "download-order-remove"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def download_remove(self, downloadId: str):
        """
        Removes an item from the download queue.
        """
        url = "{}/download-remove".format(self.endpoint)
        payload = payloads.download_remove(downloadId)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "download-remove"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def download_retrieve(self, downloadApplication=None, label=None):
        """
        Returns all available and previously requests but not completed downloads.
        """
        url = "{}/download-retrieve".format(self.endpoint)
        payload = payloads.download_retrieve(downloadApplication, label)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "download-retrieve"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def download_search(self, activeOnly=None, label=None, downloadApplication=None):
        """
        This method is used to searche for downloads within the queue,
        regardless of status, that match the given label.
        """
        url = "{}/download-search".format(self.endpoint)
        payload = payloads.download_search(activeOnly, label, downloadApplication)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "download-search"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def grid2ll(self, gridType: str, path: str, row: str, responseShape=None):
        """
        Used to translate between known grids and coordinates.
        """
        url = "{}/grid2ll".format(self.endpoint)
        payload = payloads.grid2ll(gridType, path, row, responseShape)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "grid2ll"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def permissions(self):
        """
        Returns a list of user permissions for the authenticated user.
        This method does not accept any input.
        """
        url = "{}/permissions".format(self.endpoint)
        payload = payloads.permissions()
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "permissions"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    """
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