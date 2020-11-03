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
            ✅Authn via X-Auth-Token header
            ✅Datetime for last API Key usage (invalidate key after 2 hours idle)
            ✅Optionally - set proxy headers
            Request params:
                ✅API method
                ✅payload
            ✅Response object
                ✅Getters for response params
            Handler __str__ and __repr__ methods
        API methods
            ✅Refactor existing methods to use handler
            ✅Align the list of methods with 1.5.0, remove deprecated
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

    def _get_last_response_json(self):
        """
        Get the response to last completed request as JSON.
        The data structure contains the following elements:
            - requestId: int
            - version: str (stable, development, experimental)
            - sessionId: int
            - errorCode: str
            - errorMessage: str
            - data: str (JSON)
        """
        try:
            return self.lastResponse.json()
        except AttributeError as e:
            logger.exception("Data element appears to be empty: {}".format(e))
            return

    def _get_last_response_data(self):
        """
        Get the "data" element from the last response JSON.
        Returns string/JSON.
        NOTE that some API methods return {"data": None}
        """
        j = self._get_last_response_json()
        try:
            return j["data"]
        except AttributeError as e:
            logger.exception(e)
            return       

    def _get_last_response_request_id(self):
        """
        Get the "requestId" element from the last response JSON as integer.
        """
        j = self._get_last_response_json()
        try:
            return j["requestId"]
        except AttributeError as e:
            logger.exception(e)
            return
    
    def _get_last_response_session_id(self):
        """
        Get the "sessionId" element from the last response JSON as integer.
        """
        j = self._get_last_response_json()
        try:
            return j["sessionId"]
        except AttributeError as e:
            logger.exception(e)
            return
    
    def _get_last_response_version(self):
        """
        Get the "version" element from the last response JSON as string.
        """
        j = self._get_last_response_json()
        try:
            return j["version"]
        except AttributeError as e:
            logger.exception(e)
            return
        
    def _get_last_response_error_code(self):
        """
        Get the "errorCode" element from the last response JSON as string.
        """
        j = self._get_last_response_json()
        try:
            return j["errorCode"]
        except AttributeError as e:
            logger.exception(e)
            return
    
    def _get_last_response_error_message(self):
        """
        Get the "errorMessage" element from the last response JSON as string.
        """
        j = self._get_last_response_json()
        try:
            return j["errorMessage"]
        except AttributeError as e:
            logger.exception(e)
            return

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
        """
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
        """
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
        """
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
        """
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
        """
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
        """
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
        """
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
        """
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
        """
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
        """
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

    def download_order_load(self, downloadApplication=None, label=None):
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

    def scene_list_add(self, listId: str, datasetName: str, idField=None, entityId=None, entityIds=None):
        """
        Adds items in the given scene list.
        """
        url = "{}/scene-list-add".format(self.endpoint)
        payload = payloads.scene_list_add(listId, datasetName, idField, entityId, entityIds)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "scene-list-add"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def scene_list_get(self, listId: str, datasetName=None):
        """
        Returns items in the given scene list.
        """
        url = "{}/scene-list-get".format(self.endpoint)
        payload = payloads.scene_list_get(listId, datasetName)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "scene-list-get"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def scene_list_remove(self, listId: str, datasetName=None, entityId=None, entityIds=None):
        """
        Removes items from the given list.
        """
        url = "{}/scene-list-remove".format(self.endpoint)
        payload = payloads.scene_list_remove(listId, datasetName, entityId, entityIds)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "scene-list-remove"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def scene_list_summary(self, listId: str, datasetName=None):
        """
        Returns summary information for a given list.
        """
        url = "{}/scene-list-summary".format(self.endpoint)
        payload = payloads.scene_list_summary(listId, datasetName)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "scene-list-summary"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def scene_list_types(self, listFilter=None):
        """
        Returns scene list types (exclude, search, order, bulk, etc).
        """
        url = "{}/scene-list-types".format(self.endpoint)
        payload = payloads.scene_list_types(listFilter)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "scene-list-types"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def scene_metadata(self, datasetName: str, entityId: str, metadataType=None,
                        includeNullMetadataValues=None):
        """
        This request is used to return metadata for a given scene.
        """
        url = "{}/scene-metadata".format(self.endpoint)
        payload = payloads.scene_metadata(datasetName, entityId, metadataType, includeNullMetadataValues)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "scene-metadata"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def scene_metadata_list(self, listId: str, datasetName=None, metadataType=None,
                            includeNullMetadataValues=None):
        """
        Scene Metadata where the input is a pre-set list.
        """
        url = "{}/scene-metadata-list".format(self.endpoint)
        payload = payloads.scene_metadata_list(listId, datasetName, metadataType,
                                                includeNullMetadataValues)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "scene-metadata-list"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def scene_metadata_xml(self, datasetName: str, entityId: str, metadataType=None):
        """
        Returns metadata formatted in XML, ahering to FGDC, ISO and EE scene metadata formatting standards.
        """
        url = "{}/scene-metadata-xml".format(self.endpoint)
        payload = payloads.scene_metadata_xml(datasetName, entityId, metadataType)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "scene-metadata-xml"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def scene_search(self, datasetName: str, maxResults=None, startingNumber=None, metadataType=None,
                    sortField=None, sortDirection=None, sceneFilter=None, compareListName=None,
                    bulkListName=None, orderListName=None, excludeListName=None,
                    includeNullMetadataValues=None):
        """
        Searching is done with limited search criteria. All coordinates are assumed decimal-degree format.
        If lowerLeft or upperRight are supplied, then both must exist in the request to complete the bounding box.
        Starting and ending dates, if supplied, are used as a range to search data based on acquisition dates.
        The current implementation will only search at the date level, discarding any time information.
        If data in a given dataset is composite data, or data acquired over multiple days, a search will be done
        to match any intersection of the acquisition range.
        There currently is a 50,000 scene limit for the number of results that are returned, however, some client
        applications may encounter timeouts for large result sets for some datasets.
        To use the sceneFilter field, pass one of the four search filter objects
        (SearchFilterAnd, SearchFilterBetween, SearchFilterOr, SearchFilterValue) in JSON format with sceneFilter
        being the root element of the object.
        """
        url = "{}/scene-search".format(self.endpoint)
        payload = payloads.scene_search(datasetName, maxResults, startingNumber, metadataType,
                                        sortField, sortDirection, sceneFilter, compareListName,
                                        bulkListName, orderListName, excludeListName, includeNullMetadataValues)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "scene-search"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def scene_search_delete(self, datasetName: str, maxResults=None, startingNumber=None, sortField=None,
                            sortDirection=None, temporalFilter=None):
        """
        This method is used to detect deleted scenes from datasets that support it.
        Supported datasets are determined by the 'supportDeletionSearch' parameter in the 'datasets' response.
        There currently is a 50,000 scene limit for the number of results that are returned, however, some
        client applications may encounter timeouts for large result sets for some datasets.
        """
        url = "{}/scene-search-delete".format(self.endpoint)
        payload = payloads.scene_search_delete(datasetName, maxResults, startingNumber, sortField,
                                        sortDirection, temporalFilter)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "scene-search-delete"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()

    def scene_search_secondary(self, entityId: str, datasetName: str, maxResults=None, startingNumber=None,
                            metadataType=None, sortField=None, sortDirection=None, compareListName=None,
                            bulkListName=None, orderListName=None, excludeListName=None):
        """
        This method is used to find the related scenes for a given scene.
        """
        url = "{}/scene-search-secondary".format(self.endpoint)
        payload = payloads.scene_search_secondary(entityId, datasetName, maxResults, startingNumber,
                                            metadataType, sortField, sortDirection, compareListName,
                                            bulkListName, orderListName, excludeListName)
        logger.debug("API call URL: {}".format(url))
        logger.debug("API call payload: {}".format(payload))
        headers = {"X-Auth-Token": self.apiKey}
        response = requests.post(url=url, json=payload, headers=headers, proxies=self.proxies)
        logger.debug("Received response:\n{}".format(json.dumps(response.json(), indent=4)))
        self._catch_usgs_error(response.json())
        self.lastApiMethod = "scene-search-secondary"
        self.lastRequestPayload = payload
        self.lastResponse = response
        self.lastApiKeyUseTime = dt.utcnow()
