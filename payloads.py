#!/usr/bin/env python

"""
Author: Max Solomcuk, max.solomcuk@cgi.com

Create JSON payloads for requests to the USGS Inventory API.
See https://earthexplorer.usgs.gov/inventory/documentation/json-api
"""

import json
import datamodels as DM


def cleardownloads(apiKey: str, labels=None):
    """
    Clears the pending downloads from the users download queue.
    https://earthexplorer.usgs.gov/inventory/documentation/json-api?version=1.4.1#cleardownloads

    :param apiKey:
        String. Users API Key/Authentication Token. Obtained from login request - this can be ommitted
        when using the 'X-Auth-Token' header to pass this value.
    :param labels:
        List of strings. Used to filter downloads by a specific id (per user). An array of label strings.
    """

    payload = {
        'apiKey': apiKey
    }

    if labels:
        payload['labels'] = labels

    return json.dumps(payload)

def datasetfields(apiKey: str, datasetName=None):
    """
    This request is used to return the metadata filter fields for the specified dataset.
    These values can be used as additional criteria when submitting search and hit queries.
    https://earthexplorer.usgs.gov/inventory/documentation/json-api?version=1.4.1#datasetfields

    :param apiKey:
        String. Users API Key/Authentication Token. Obtained from login request - this can be ommitted
        when using the 'X-Auth-Token' header to pass this value
    :param datasetName:
        String. Identifies the dataset. Use the datasetName from datasets response
    """

    payload = {
        'apiKey': apiKey,
    }

    if datasetName:
        payload['datasetName'] = datasetName

    return json.dumps(payload)

def datasets(apiKey: str, datasetName=None, spatialFilter=None, temporalFilter=None, publicOnly=False):
    """
    This method is used to find datasets available for searching. By passing only API Key,
    all available datasets are returned. Additional parameters such as temporal range and
    spatial bounding box can be used to find datasets that provide more specific data. The
    dataset name parameter can be used to limit the results based on matching the supplied
    value against the public dataset name with assumed wildcards at the beginning and end.
    https://earthexplorer.usgs.gov/inventory/documentation/json-api?version=1.4.1#datasets

    :param apiKey:
        String. Users API Key/Authentication Token. Obtained from login request - this can be ommitted
        when using the 'X-Auth-Token' header to pass this value
    :param datasetName:
        String. Used as a filter with wildcards inserted at the beginning and the end of the supplied value.
        Compared against public dataset names internal datasetName, and IDN Entry ID Fields
    :param spatialFilter:
        SpatialFilter. Used to apply a spatial filter on the data
    :param temporalFilter:
        TemporalFilter. Used to apply a temporal filter on the data
    :param publicOnly:
        Boolean. Used to filter out datasets that are not accessible to unauthenticated users.
    """

    payload = {
        'apiKey': apiKey
    }

    if datasetName:
        payload['datasetName'] = datasetName

    if spatialFilter:
        payload['spatialFilter'] = spatialFilter

    if temporalFilter:
        payload['temporalFilter'] = temporalFilter

    if publicOnly:
        payload['publicOnly'] = publicOnly

    return json.dumps(payload)

def deletionsearch(apiKey: str, datasetName: str, temporalFilter=None, additionalCriteria=None, maxResults=10, startingNumber=1, sortOrder='ASC'):
    """
    This method is used to detect deleted scenes from datasets that support it. Supported datasets
    are determined by the 'supportDeletionInventory' parameter in the 'datasets' response. There
    currently is a 50,000 scene limit for the number of results that are returned, however, some
    client applications may encounter timeouts for large result sets for some datasets.

    To use the additional criteria field, pass one of the four search filter objects
    (SearchFilterAnd, SearchFilterBetween, SearchFilterOr, SearchFilterValue) in JSON format with
    additionalCriteria being the root element of the object. 

    https://earthexplorer.usgs.gov/inventory/documentation/json-api?version=1.4.1#deletionsearch

    :param apiKey:
        String. Users API Key/Authentication Token. Obtained from login request - this can be ommitted
        when using the 'X-Auth-Token' header to pass this value.
    :param datasetName:
        String. Identifies the dataset. Use the datasetName from datasets response.
    :param temporalFilter:
        TemporalFilter. Used to apply a temporal filter on the data. Use 'deleted' for the 'dateField' parameter.
    :param additionalCriteria:
        SearchFilter list. Optional additional request criteria.
    :param maxResults:
        Integer. Used to determine the number of results to return. Use with startingNumber for controlled
        pagination. Maximum list size - 50,000.
    :param startingNumber:
        Integer. Used to determine the result number to start returning from. Use with maxResults for
        controlled pagination.
    :param sortOrder:
        String. Used to order results based on acquisition date. Accepted values are "ASC" and "DESC".
    """

    payload = {
        'apiKey': apiKey,
        'datasetName': datasetName,
        'maxResults': maxResults,
        'startingNumber': startingNumber,
        'sortOrder': sortOrder
    }

    if temporalFilter:
        payload['temporalFilter'] = temporalFilter
    
    if additionalCriteria:
        payload['additionalCriteria'] = additionalCriteria

    return json.dumps(payload)

def grid2ll(gridType: str, responseShape: str, path: int, row: int):
    """
    Used to translate between known grids and coordinates.
    https://earthexplorer.usgs.gov/inventory/documentation/json-api?version=1.4.1#grid2ll

    :param gridType:
        String. Identifies the grid system. Accepted values: 'WRS1' and 'WRS2'
    :param responseShape:
        String. Determines if the response should be a center point or outer polygon.
        Accepted values: 'point' and 'polygon'
    :param path:
        Integer. WRS 1/2 Path. Required for WRS lookups.
    :param row:
        Integer. WRS 1/2 Path. Required for WRS lookups.
    """

    return json.dumps({
        'gridType': gridType,
        'responseShape': responseShape,
        'path': path,
        'row': row
    })

def idlookup(apiKey: str, datasetName: str, idList: list, inputField='entityId'):
    """
    Given a dataset, ID type, and scene list, this method will translate from one ID type to the other.
    https://earthexplorer.usgs.gov/inventory/documentation/json-api?version=1.4.1#idlookup

    :param apiKey:
        String. Users API Key/Authentication Token. Obtained from login request - this can be ommitted
        when using the 'X-Auth-Token' header to pass this value.
    :param datasetName:
        String. Identifies the dataset. Use the datasetName from datasets response.
    :param idList:
        List of strings. Identifies scenes ID's to lookup. Maximum list size - 50,000.
    :param inputField:
        String. Used to define the ID field to translate from. Accepted values are 'entityId' and 'displayId'.
    """

    return json.dumps({
        'apiKey': apiKey,
        'datasetName': datasetName,
        'idList': idList,
        'inputField': inputField
    })

def login(username: str, password: str, catalogId='EE', applicationContext=None, authType='EROS'):
    """
    Upon a successful login, an API key will be returned. This key will be active for one hour and
    should be destroyed upon final use of the service by calling the logout method.

    This request requires an HTTP POST request instead of a HTTP GET request as a security measure
    to prevent username and password information from being logged by firewalls, web servers, etc. 
    https://earthexplorer.usgs.gov/inventory/documentation/json-api?version=1.4.1#login

    :param username:
        String. Your USGS registration username.
    :param password:
        String. Your USGS registration password.
    :param catalogId:
        String. Determines the dataset catalog to use.
    :param applicationContext:
        String. Used to identify the application which this demographic should belong to.
    :param authType:
        String. Default value "EROS". Not sure what's the usage here.
    """

    payload = {
        'username': username,
        'password': password,
        'catalogId': catalogId,
        'authType': authType
    }

    if applicationContext:
        payload['applicationContext'] = applicationContext

    return json.dumps(payload)

def logout(apiKey: str):
    """
    This method is used to remove the users API key from being used in the future.
    https://earthexplorer.usgs.gov/inventory/documentation/json-api?version=1.4.1#logout

    :param apiKey:
        String. Users API Key/Authentication Token. Obtained from login request - this can be ommitted
        when using the 'X-Auth-Token' header to pass this value.
    """

    return json.dumps({
        'apiKey': apiKey
    })

def notifications(apiKey):
    """
    This method returns all system notifications for the current application context.
    https://earthexplorer.usgs.gov/inventory/documentation/json-api?version=1.4.1#notifications
    
    :param apiKey:
        String. Users API Key/Authentication Token. Obtained from login request - this can be ommitted
        when using the 'X-Auth-Token' header to pass this value.
    """
    
    return json.dumps({
        'apiKey': apiKey
    })

def metadata(apiKey: str, datasetName: str, entityIds: list, includeDataAccess=False, includeBrowse=True, includeSpatial=True):
    """
    The download options request is used to discover downloadable products for each dataset.
    If a download is marked as not available, an order must be placed to generate that product.
    https://earthexplorer.usgs.gov/inventory/documentation/json-api?version=1.4.1#metadata

    :param apiKey:
        String. Users API Key/Authentication Token. Obtained from login request - this can be ommitted
        when using the 'X-Auth-Token' header to pass this value.
    :param datasetName:
        String. Identifies the dataset. Use the datasetName from datasets response.
    :param entityIds:
        Boolean. Identifies one or more scenes to gather metadata for. Maximum list size - 50,000.
    :param includeDataAccess:
        Boolean. Denotes if data access URLs should be returned for each scene.
    :param includeBrowse:
        Boolean. Denotes if browse links should be returned for each scene.
    :param includeSpatial:
        Boolean. Denotes if spatial information should be returned for each scene.
    """

    payload = {
        'apiKey': apiKey,
        'datasetName': datasetName,
        'entityIds': entityIds
    }

    if includeDataAccess:
        payload['includeDataAccess'] = includeDataAccess

    if includeBrowse:
        payload['includeBrowse'] = includeBrowse
    
    if includeSpatial:
        payload['includeSpatial'] = includeSpatial

    return json.dumps(payload)

def search(apiKey: str, datasetName: str, spatialFilter=None, temporalFilter=None, metadataUpdateFilter=None, months=None, includeBrowse=True,
        includeSpatial=True, includeUnknownCloudCover=True, minCloudCover=0, maxCloudCover=100, additionalCriteria=None, maxResults=10,
        responseFormat='standard', startingNumber=1, sortField='acquisitionDate', sortOrder='ASC'):
    """
    Searching is done with limited search criteria. All coordinates are assumed decimal-degree format.
    If lowerLeft or upperRight are supplied, then both must exist in the request to complete the bounding
    box. Starting and ending dates, if supplied, are used as a range to search data based on acquisition
    dates. The current implementation will only search at the date level, discarding any time information.
    If data in a given dataset is composite data, or data acquired over multiple days, a search will be
    done to match any intersection of the acquisition range. There currently is a 50,000 scene limit for
    the number of results that are returned, however, some client applications may encounter timeouts for
    large result sets for some datasets.

    To use the additional criteria field, pass one of the four search filter objects (SearchFilterAnd,
    SearchFilterBetween, SearchFilterOr, SearchFilterValue) in JSON format with additionalCriteria being
    the root element of the object.
    https://earthexplorer.usgs.gov/inventory/documentation/json-api?version=1.4.1#search

    :param apiKey:
        String. Users API Key/Authentication Token. Obtained from login request - this can be ommitted
        when using the 'X-Auth-Token' header to pass this value.
    :param datasetName:
        String. Identifies the dataset. Use the datasetName from datasets response.
    :param spatialFilter:
        SpatialFilter. Used to apply a spatial filter on the data.
    :param temporalFilter:
        TemporalFilter. Used to apply a temporal filter on the data.
    :param metadataUpdateFilter:
        TemporalFilter. Used to filter scenes by last metadata update.
    :param months:
        List of integers. Used to limit results to specific months. Valid values are [1,12].
    :param includeBrowse:
        Boolean. Used to determine if browse links are returned. Setting this to false will result in faster response times.
    :param includeSpatial:
        Boolean. Used to determine if geospatial metadata is returne. Setting this to false will result in faster response times.
    :param includeUnknownCloudCover:
        Boolean. Used to determine if scenes with unknown cloud cover values should be included in the results.
    :param minCloudCover:
        Boolean. Used to limit results by minimum cloud cover (for supported datasets). Valid values are [0, 100].
    :param maxCloudCover:
        Boolean. Used to limit results by maximum cloud cover (for supported datasets). Valid values are [0, 100].
    :param additionalCriteria:
        SearchFilter. Used to filter results based on dataset specific metadata fields.
        Use datasetFields request to determine available fields and options.
    :param maxResults:
        Integer. Used to determine the number of results to return. Use with startingNumber for controlled pagination.
        Maximum list size - 50,000
    :param responseFormat:
        String. Used to determine what is included in the response. 'standard' and 'sceneList' are valid values.
        The scene list resposne only includes an array of entityId values for matching scenes under the results property.
    :param startingNumber:
        Integer. Used to determine the result number to start returning from. Use with maxResults for controlled pagination.
    :param sortField:
        String. Used to define the field to sort the result set. Valid values are 'acquisitionDate', 'displayId' or 'modifiedDate'.
    :param sortOrder:
        String. Used to order results based on acquisition date.
    """

    payload = {
        'apiKey': apiKey,
        'datasetName': datasetName,
        'includeBrowse': includeBrowse,
        'includeSpatial': includeSpatial,
        'includeUnknownCloudCover': includeUnknownCloudCover,
        'minCloudCover': minCloudCover,
        'maxCloudCover': maxCloudCover,
        'maxResults': maxResults,
        'responseFormat': responseFormat,
        'startingNumber': startingNumber,
        'sortField': sortField,
        'sortOrder': sortOrder
    }

    if spatialFilter:
        payload['spatialFilter'] = spatialFilter
    
    if temporalFilter:
        payload['temporalFilter'] = temporalFilter

    if metadataUpdateFilter:
        payload['metadataUpdateFilter'] = metadataUpdateFilter

    if months:
        payload['months'] = months

    if additionalCriteria:
        payload['additionalCriteria'] = additionalCriteria

    return json.dumps(payload)

def hits(apiKey: str, datasetName: str, spatialFilter=None, temporalFilter=None, metadataUpdateFilter=None, months=None,
        includeUnknownCloudCover=True, minCloudCover=0, maxCloudCover=100, additionalCriteria=None):
    """
    This method is used in determining the number of hits a search returns. Because a hits request requires a search,
    this request takes the same parameters as the search request, with exception to the non-search-field parameters:
    maxResults, startingNumber, sortField and sortOrder.
    https://earthexplorer.usgs.gov/inventory/documentation/json-api?version=1.4.1#hits

    :param apiKey:
        String. Users API Key/Authentication Token. Obtained from login request - this can be ommitted
        when using the 'X-Auth-Token' header to pass this value.
    :param datasetName:
        String. Identifies the dataset. Use the datasetName from datasets response.
    :param spatialFilter:
        SpatialFilter. Used to apply a spatial filter on the data.
    :param temporalFilter:
        TemporalFilter. Used to apply a temporal filter on the data.
    :param metadataUpdateFilter:
        TemporalFilter. Used to filter scenes by last metadata update.
    :param months:
        List of integers. Used to limit results to specific months. Valid values are [1,12].
    :param includeUnknownCloudCover:
        Boolean. Used to determine if scenes with unknown cloud cover values should be included in the results.
    :param minCloudCover:
        Boolean. Used to limit results by minimum cloud cover (for supported datasets). Valid values are [0, 100].
    :param maxCloudCover:
        Boolean. Used to limit results by maximum cloud cover (for supported datasets). Valid values are [0, 100].
    :param additionalCriteria:
        SearchFilter. Used to filter results based on dataset specific metadata fields.
        Use datasetFields request to determine available fields and options.
    """

    payload = {
        'apiKey': apiKey,
        'datasetName': datasetName,
        'includeUnknownCloudCover': includeUnknownCloudCover,
        'minCloudCover': minCloudCover,
        'maxCloudCover': maxCloudCover,
    }

    if spatialFilter:
        payload['spatialFilter'] = spatialFilter
    
    if temporalFilter:
        payload['temporalFilter'] = temporalFilter

    if metadataUpdateFilter:
        payload['metadataUpdateFilter'] = metadataUpdateFilter

    if months:
        payload['months'] = months

    if additionalCriteria:
        payload['additionalCriteria'] = additionalCriteria

    return json.dumps(payload)

def status():
    """
    This method is used to get the status of the API. There are no parameters available to call this method with.
    https://earthexplorer.usgs.gov/inventory/documentation/json-api?version=1.4.1#status
    Implemented as a dummy method with empty return to keep things consistent.
    """
    return json.dumps({})

def download(apiKey: str, datasetName: str, entityIds: list, products: list):
    """
    :param apiKey:
        String. Users API Key/Authentication Token. Obtained from login request - this can be ommitted
        when using the 'X-Auth-Token' header to pass this value.
    :param datasetName:
        String. Identifies the dataset. Use the datasetName from datasets response.
    :param entityIds:
        List of strings.
    :param products:
        List of strings. Product types to download for specified entityIds
    """
    return json.dumps({
        'apiKey': apiKey,
        'datasetName': datasetName,
        'entityIds': entityIds,
        'products': products
    })

def downloadoptions(apiKey: str, datasetName: str, entityIds: list):
    """
    :param apiKey:
        String. Users API Key/Authentication Token. Obtained from login request - this can be ommitted
        when using the 'X-Auth-Token' header to pass this value.
    :param datasetName:
        String. Identifies the dataset. Use the datasetName from datasets response.
    :param entityIds:
        List of strings
    """

    return json.dumps({
        'apiKey': apiKey,
        'datasetName': datasetName,
        'entityIds': entityIds
    })
