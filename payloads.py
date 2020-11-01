#!/usr/bin/env python

"""
Author: Max Solomcuk, max.solomcuk@cgi.com

Create payloads (as Python dictionaries) for requests to the USGS Inventory API.
See https://m2m.cr.usgs.gov/api/docs/json/
"""


def data_owner(dataOwner: str):
    """
    This method is used to provide the contact information of the data owner.
    https://m2m.cr.usgs.gov/api/docs/reference/#data-owner

    :param dataOwner:
        String. Required.   Used to identify the data owner - this value comes from the
                            dataset-search response.
    """
    return {"dataOwner": dataOwner}

def dataset(datasetId = None, datasetName = None):
    """
    This method is used to retrieve the dataset by id or name.
    https://m2m.cr.usgs.gov/api/docs/reference/#dataset

    Only one parameter must be provided.

    :param datasetId:
        String. Optional.   The dataset identifier - must use this or datasetName.
    :param datasetName:
        String. Optional.   The system-friendly dataset name - must use this or datasetId.
    """
    if datasetId and datasetName:
        raise ValueError("Use only one of datasetId or datasetName, not both.")
    elif (not datasetId) and (not datasetName):
        raise ValueError("One of datasetId or datasetName is required.")
    elif datasetId:
        return {"datasetId": datasetId}
    elif datasetName:
        return {"datasetName": datasetName}

def dataset_categories(catalog=None, includeMessages=None, publicOnly=None, parentId=None, datasetFilter=None):
    """
    This method is used to search datasets under the categories.
    https://m2m.cr.usgs.gov/api/docs/reference/#dataset-caterogies

    At least one of the catalog, parentId, or datasetFilter must be provided.

    :param catalog:
        String. Optional.   Used to identify datasets that are associated with a given application.
    :param includeMessages:
        Boolean. Optional.  Optional parameter to include messages regarding specific dataset components.
    :param publicOnly:
        Boolean. Optional.  Used as a filter out datasets that are not accessible to unauthenticated 
                            general public users.
    :param parentId:
        String. Optional.   If provided, returned categories are limited to categories that are children
                            of the provided ID.
    :param datasetFilter:
        String. Optional.   If provided, filters the datasets - this automatically adds a wildcard before
                            and after the input value.
    """
    payload = {}
    if catalog:
        payload["catalog"] = catalog
    if includeMessages:
        payload["includeMessages"] = includeMessages
    if publicOnly:
        payload["publicOnly"] = publicOnly
    if parentId:
        payload["parentId"] = parentId
    if datasetFilter:
        payload["datasetFilter"] = datasetFilter
    
    return payload

def dataset_coverage(datasetName: str):
    """
    Returns coverage for a given dataset.
    https://m2m.cr.usgs.gov/api/docs/reference/#dataset-coverage

    :param datasetName:
        String. Required.   Determines which dataset to return coverage for.
    """
    return {"datasetName": datasetName}

def dataset_filters(datasetName: str):
    """
    This request is used to return the metadata filter fields for the specified dataset.
    These values can be used as additional criteria when submitting search and hit queries.
    https://m2m.cr.usgs.gov/api/docs/reference/#dataset-filters

    :param datasetName:
        String. Required.   Determines which dataset to return filters for.
    """
    return {"datasetName": datasetName}

def dataset_messages(catalog=None, datasetName=None, datasetNames=None):
    """
    Returns any notices regarding the given datasets features.
    https://m2m.cr.usgs.gov/api/docs/reference/#dataset-messages

    At least one of the catalog, datasetName, or datasetNames must be provided.

    :param catalog:
        String. Optional.   Used to identify datasets that are associated with a given
                            application.
    :param datasetName:
        String. Optional.   Used as a filter with wildcards inserted at the beginning
                            and the end of the supplied value.
    :param datasetNames:
        String[]. Optional. Used as a filter with wildcards inserted at the beginning
                            and the end of the supplied value.
    """
    if (not catalog) and (not datasetName) and (not datasetNames):
        raise ValueError("At least one of catalog, datasetName, or datasetNames must be provided.")
    payload = {}
    if catalog:
        payload["catalog"] = catalog
    if datasetName:
        payload["datasetName"] = datasetName
    if datasetNames:
        payload["datasetNames"] = datasetNames

    return payload

def dataset_search(catalog=None, categoryId=None, datasetName=None, includeMessages=None,
                    publicOnly=None, includeUnknownSpatial=None, temporalFilter=None, spatialFilter=None):
    """
    This method is used to find datasets available for searching. By passing only API Key, all available
    datasets are returned. Additional parameters such as temporal range and spatial bounding box can be
    used to find datasets that provide more specific data. The dataset name parameter can be used to limit
    the results based on matching the supplied value against the public dataset name with assumed wildcards
    at the beginning and end.
    https://m2m.cr.usgs.gov/api/docs/reference/#dataset-search

    :param catalog:
        String. Optional.   Used to identify datasets that are associated with a given
                            application.
    :param categoryId:
        String. Optional.   Used to restrict results to a specific category (does not
                            search sub-sategories).
    :param datasetName:
        String. Optional.   Used as a filter with wildcards inserted at the beginning
                            and the end of the supplied value.
    :param includeMessages:
        Boolean. Optional.  Optional parameter to include messages regarding specific
                            dataset components.
    :param publicOnly:
        Boolean. Optional.  Used as a filter out datasets that are not accessible to
                            unauthenticated general public users.
    :param includeUnknownSpatial:
        Boolean. Optional.  Optional parameter to include datasets that do not support
                            geographic searching.
    :param temporalFilter:
        TemporalFilter*. Optional.  Used to filter data based on data acquisition.
    :param spatialFilter:
        SpatialFilter**. Optional.  Used to filter data based on data location.

    *  https://m2m.cr.usgs.gov/api/docs/datatypes/#temporalFilter
    ** https://m2m.cr.usgs.gov/api/docs/datatypes/#spatialFilter
    """
    payload = {}

    if catalog:
        payload["catalog"] = catalog
    if categoryId:
        payload["categoryId"] = categoryId
    if datasetName:
        payload["datasetName"] = datasetName
    if includeMessages:
        payload["includeMessages"] = includeMessages
    if publicOnly:
        payload["publicOnly"] = publicOnly
    if includeUnknownSpatial:
        payload["includeUnknownSpatial"] = includeUnknownSpatial
    if temporalFilter:
        payload["temporalFilter"] = temporalFilter
    if spatialFilter:
        payload["spatialFilter"] = spatialFilter
    
    return payload

def download_labels(downloadApplication=None):
    """
    Gets a list of unique download labels associated with the orders.
    https://m2m.cr.usgs.gov/api/docs/reference/#download-labels

    :param downloadApplication:
        String. Optional.   Used to denote the application that will perform the download.
    """
    payload = {}
    if downloadApplication:
        payload["downloadApplication"] = downloadApplication
    
    return payload

def download_order_load(downloadApplication=None, label=None):
    """
    This method is used to prepare a download order for processing by moving the scenes into
    the queue for processing.
    https://m2m.cr.usgs.gov/api/docs/reference/#download-order-load

    :param downloadApplication:
        String. Optional.   Used to denote the application that will perform the download.
    :param label:
        String[]. Optional.   Determines which order to load. (TODO: check if can be a list)
    """
    payload = {}
    if downloadApplication:
        payload["downloadApplication"] = downloadApplication
    if label:
        payload["label"] = label

    return payload

def download_order_remove(label: str, downloadApplication=None):
    """
    This method is used to remove an order from the download queue.
    https://m2m.cr.usgs.gov/api/docs/reference/#download-order-remove

    :param downloadApplication:
        String. Optional.   Used to denote the application that will perform the download.
    :param label:
        String. Required.   Determines which order to remove.
    """
    payload = {"label": label}
    if downloadApplication:
        payload["downloadApplication"] = downloadApplication
    
    return payload

def download_remove(downloadId: int):
    """
    Removes an item from the download queue.
    https://m2m.cr.usgs.gov/api/docs/reference/#download-remove

    :param downloadId:
        Integer. Required.  Represents the ID of the download from within the queue.
    
    Note: "downloadId" can be retrieved by calling download-search
    """
    return {"downloadId": downloadId}

def download_retrieve(downloadApplication=None, label=None):
    """
    Returns all available and previously requests but not completed downloads.
    https://m2m.cr.usgs.gov/api/docs/reference/#download-retrieve

    :param downloadApplication:
        String. Optional.   Used to denote the application that will perform the download.
    :param label:
        String. Optional.   Determines which downloads to return.
    """
    payload = {}
    if downloadApplication:
        payload["downloadApplication"] = downloadApplication
    if label:
        payload["label"] = label
    
    return payload

def download_search(activeOnly=None, label=None, downloadApplication=None):
    """
    This method is used to search for downloads within the queue, regardless of status,
    that match the given label.
    https://m2m.cr.usgs.gov/api/docs/reference/#download-search

    :param activeOnly:
        Boolean. Optional.  Determines if completed, failed, cleared and proxied downloads
                            are returned.
    :param downloadApplication:
        String. Optional.   Used to filter downloads by the intended downloading application.
    :param label:
        String. Optional.   Used to filter downloads by label.
    """
    payload = {}
    if activeOnly:
        payload["activeOnly"] = activeOnly
    if label:
        payload["label"] = label
    if downloadApplication:
        payload["downloadApplication"] = downloadApplication
    
    return payload

def grid2ll(gridType: str, path: str, row: str, responseShape=None):
    """
    Used to translate between known grids and coordinates.
    https://m2m.cr.usgs.gov/api/docs/reference/#grid2ll

    :param gridType:
        String. Required.   Which grid system is being used? (WRS1 or WRS2)
    :param responseShape:
        String. Optional.   What type of geometry should be returned -
                            a bounding box polygon or a center point? (polygon or point)
    :param path:
        String. Required.   The x coordinate in the grid system.
    :param row:
        String. Required.   The y coordinate in the grid system.

    Note that the API doc page lists both path and row as optional - this is probably not true.
    Sending this request without either path or row returns an error with a message that they are 
    required.
    """

    payload = {
        "gridType": gridType,
        "path": path,
        "row": row
    }
    if responseShape:
        payload["responseShape"] = responseShape
    
    return payload

def login(username: str, password: str, userContext=None):
    """
    Upon a successful login, an API key will be returned. This key will be active for two hours and
    should be destroyed upon final use of the service by calling the logout method.

    This request requires an HTTP POST request instead of a HTTP GET request as a security measure
    to prevent username and password information from being logged by firewalls, web servers, etc. 
    https://m2m.cr.usgs.gov/api/docs/reference/#login

    :param username:
        String. Required.   ERS username.
    :param password:
        String. Required.   ERS password.
    :param userContext:
        UserContext*. Optional. Metadata describing the user the request is on behalf of.
    
    *  https://m2m.cr.usgs.gov/api/docs/datatypes/#userContext
    """

    payload = {
        "username": username,
        "password": password
    }

    if userContext:
        payload["userContext"] = userContext

    return payload

def logout():
    """
    This method is used to remove the user's API key from being used in the future.
    https://m2m.cr.usgs.gov/api/docs/reference/#logout

    This request does not use request parameters and does not return a data value.
    """

    return {}

def notifications(systemId: str):
    """
    Gets a notification list.
    https://m2m.cr.usgs.gov/api/docs/reference/#notifications
    
    :param systemId:
        String. Required.   Determines the system you wish to return notifications for.
    """
    
    return {"systemId": systemId}

def permissions():
    """
    Returns a list of user permissions for the authenticated user. This method does not
    accept any input.
    https://m2m.cr.usgs.gov/api/docs/reference/#permissions
    """
    return {}

def scene_list_add(listId: str, datasetName: str, idField=None, entityId=None, entityIds=None):
    """
    Adds items in the given scene list.
    https://m2m.cr.usgs.gov/api/docs/reference/#scene-list-add

    :param listId:
        String. Required.   User defined name for the list.
    :param datasetName:
        String. Required.   Dataset alias.
    :param idField:
        String. Optional.   Used to determine which ID is being used - entityId (default) or displayId.
    :param entityId:
        String. Optional.   Scene identifier.
    :param entityIds:
        String[]. Optional. A list of scene identifiers.
    """
    payload = {
        "listId": listId,
        "datasetName": datasetName
    }
    if idField:
        payload["idField"] = idField
    if entityId:
        payload["entityId"] = entityId
    if entityIds:
        payload["entityIds"] = entityIds
    
    return payload

def scene_list_get(listId: str, datasetName=None):
    """
    Returns items in the given scene list.
    https://m2m.cr.usgs.gov/api/docs/reference/#scene-list-get

    :param listId:
        String. Required.   User defined name for the list.
    :param datasetName:
        String. Optional.   Dataset alias.
    """
    payload = {
        "listId": listId
    }
    if datasetName:
        payload["datasetName"] = datasetName

    return payload

def scene_list_remove(listId: str, datasetName=None, entityId=None, entityIds=None):
    """
    Removes items from the given list.
    https://m2m.cr.usgs.gov/api/docs/reference/#scene-list-remove

    :param listId:
        String. Required.   User defined name for the list.
    :param datasetName:
        String. Optional.   Dataset alias.
    :param entityId:
        String. Optional.   Scene indentifier.
    :param entityIds:
        String[]. Optional. A list of scene identifiers.
    """
    payload = {
        "listId": listId
    }
    if datasetName:
        payload["datasetName"] = datasetName
    if entityId:
        payload["entityId"] = entityId
    if entityIds:
        payload["entityIds"] = entityIds

    return payload

def scene_list_summary(listId:str, datasetName=None):
    """
    Returns summary information for a given list.
    https://m2m.cr.usgs.gov/api/docs/reference/#scene-list-summary

    :param listId:
        String. Required.   User defined name for the list.
    :param datasetName:
        String. Optional.   Dataset alias.
    """
    payload = {
        "listId": listId
    }
    if datasetName:
        payload["datasetName"] = datasetName

    return payload

def scene_list_types(listFilter=None):
    """
    Returns scene list types (exclude, search, order, bulk, etc).
    https://m2m.cr.usgs.gov/api/docs/reference/#scene-list-types

    :param listFilter:
        String. Optional.   If provided, only returns listIds that have the provided filter
                            value within the ID.
    """
    payload = {}
    if listFilter:
        payload["listFilter"] = listFilter
    
    return payload

def scene_metadata(datasetName: str, entityId: str, metadataType=None, includeNullMetadataValues=None):
    """
    This request is used to return metadata for a given scene.
    https://m2m.cr.usgs.gov/api/docs/reference/#scene-metadata

    :param datasetName:
        String. Required.   Used to identify the dataset to search.
    :param entityId:
        String. Required.   Used to identify the scene to return results for.
    :param metadataType:
        String. Optional.   If populated, identifies which metadata to return (summary, full, fgdc, iso).
    :param includeNullMetadataValues:
        Boolean. Optional.  Optional parameter to include null metadata values.
    """
    payload = {
        "datasetName": datasetName,
        "entityId": entityId
    }
    if metadataType:
        payload["metadataType"] = metadataType
    if includeNullMetadataValues:
        payload["includeNullMetadataValues"] = includeNullMetadataValues
    
    return payload

def scene_metadata_list(listId: str, datasetName=None, metadataType=None, includeNullMetadataValues=None):
    """
    Scene Metadata where the input is a pre-set list.
    https://m2m.cr.usgs.gov/api/docs/reference/#scene-metadata-list

    :param datasetName:
        String. Optional.   Used to identify the dataset to search.
    :param listId:
        String. Required.   Used to identify the list of scenes to use.
    :param metadataType:
        String. Optional.   If populated, identifies which metadata to return (summary or full).
    :param includeNullMetadataValues:
        Boolean. Optional.  Optional parameter to include null metadata values.
    """
    payload = {
        "listId": listId
    }
    if datasetName:
        payload["datasetName"] = datasetName
    if metadataType:
        payload["metadataType"] = metadataType
    if includeNullMetadataValues:
        payload["includeNullMetadataValues"] = includeNullMetadataValues
    
    return payload

def scene_metadata_xml(datasetName: str, entityId: str, metadataType=None):
    """
    Returns metadata formatted in XML, adhering to FGDC, ISO and EE scene metadata formatting standards.
    https://m2m.cr.usgs.gov/api/docs/reference/#scene-metadata-xml

    :param datasetName:
        String. Required.   Used to identify the dataset to search.
    :param entityId:
        String. Required.   Used to identify the scene to return results for.
    :param metadataType:
        String. Optional.   If populated, identifies which metadata to return (full, fgdc, iso).
    """
    payload = {
        "datasetName": datasetName,
        "entityId": entityId
    }
    if metadataType:
        payload["metadataType"] = metadataType
    
    return payload

def scene_search(datasetName: str, maxResults=None, startingNumber=None, metadataType=None, sortField=None,
                sortDirection=None, sceneFilter=None, compareListName=None, bulkListName=None,
                orderListName=None, excludeListName=None, includeNullMetadataValues=None):
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
    https://m2m.cr.usgs.gov/api/docs/reference/#scene-search

    :param datasetName:
        String. Required.   Used to identify the dataset to search.
    :param maxResults:
        Integer. Optional.  How many results should be returned? (default = 100).
    :param startingNumber:
        Integer. Optional.  Used to identify the start number to search from.
    :param metadataType:
        String. Optional.   If populated, identifies which metadata to return (summary or full).
    :param sortField:
        String. Optional.   Determines which field to sort the results on.
    :param sortDirection:
        String. Optional.   Determines how the results should be sorted - ASC or DESC.
    :param sceneFilter:
        SceneFilter*. Optional.  Used to filter data within the dataset.
    :param compareListName:
        String. Optional.   If provided, defined a scene-list listId to use to track scenes selected for comparison.
    :param bulkListName:
        String. Optional.   If provided, defined a scene-list listId to use to track scenes selected for bulk ordering.
    :param orderListName:
        String. Optional.   If provided, defined a scene-list listId to use to track scenes selected for on-demand ordering.
    :param excludeListName:
        String. Optional.   If provided, defined a scene-list listId to use to exclude scenes from the results.
    :param includeNullMetadataValues:
        Boolean. Optional.  Optional parameter to include null metadata values.
    
    *  https://m2m.cr.usgs.gov/api/docs/datatypes/#sceneFilter
    """
    payload = {
        "datasetName": datasetName
    }
    if maxResults:
        payload["maxResults"] = maxResults
    if startingNumber:
        payload["startingNumber"] = startingNumber
    if metadataType:
        payload["metadataType"] = metadataType
    if sortField:
        payload["sortField"] = sortField
    if sortDirection:
        payload["sortDirection"] = sortDirection
    if sceneFilter:
        payload["sceneFilter"] = sceneFilter
    if compareListName:
        payload["compareListName"] = compareListName
    if bulkListName:
        payload["bulkListName"] = bulkListName
    if orderListName:
        payload["orderListName"] = orderListName
    if excludeListName:
        payload["excludeListName"] = excludeListName
    if includeNullMetadataValues:
        payload["includeNullMetadataValues"] = includeNullMetadataValues

    return payload

def scene_search_delete(datasetName: str, maxResults=None, startingNumber=None, sortField=None,
                        sortDirection=None, temporalFilter=None):
    """
    This method is used to detect deleted scenes from datasets that support it.
    Supported datasets are determined by the 'supportDeletionSearch' parameter in the 'datasets' response.
    There currently is a 50,000 scene limit for the number of results that are returned, however, some
    client applications may encounter timeouts for large result sets for some datasets.
    https://m2m.cr.usgs.gov/api/docs/reference/#scene-search-delete

    :param datasetName:
        String. Required.   Used to identify the dataset to search.
    :param maxResults:
        Integer. Optional.  How many results should be returned? (default = 100).
    :param startingNumber:
        Integer. Optional.  Used to identify the start number to search from.
    :param sortField:
        String. Optional.   Determines which field to sort the results on.
    :param sortDirection:
        String. Optional.   Determines how the results should be sorted - ASC or DESC.
    :param temporalFilter:
        TemporalFilter*. Optional.   Used to filter data based on data acquisition.

    *  https://m2m.cr.usgs.gov/api/docs/datatypes/#temporalFilter
    """
    payload = {
        "datasetName": datasetName
    }
    if maxResults:
        payload["maxResults"] = maxResults
    if startingNumber:
        payload["startingNumber"] = startingNumber
    if sortField:
        payload["sortField"] = sortField
    if sortDirection:
        payload["sortDirection"] = sortDirection
    if temporalFilter:
        payload["temporalFilter"] = temporalFilter
    
    return payload

def scene_search_secondary(entityId: str, datasetName: str, maxResults=None, startingNumber=None,
                            metadataType=None, sortField=None, sortDirection=None, compareListName=None,
                            bulkListName=None, orderListName=None, excludeListName=None):
    """
    This method is used to find the related scenes for a given scene.
    https://m2m.cr.usgs.gov/api/docs/reference/#scene-search-secondary

    :param entityId:
        String. Required.   Used to identify the scene to find related scenes for.
    :param datasetName:
        String. Required.   Used to identify the dataset to search.
    :param maxResults:
        Integer. Optional.  How many results should be returned? (default = 100).
    :param startingNumber:
        Integer. Optional.  Used to identify the start number to search from.
    :param metadataType:
        String. Optional.   If populated, identifies which metadata to return (summary or full).
    :param sortField:
        String. Optional.   Determines which field to sort the results on.
    :param sortDirection:
        String. Optional.   Determines how the results should be sorted - ASC or DESC.
    :param compareListName:
        String. Optional.   If provided, defined a scene-list listId to use to track scenes selected for comparison.
    :param bulkListName:
        String. Optional.   If provided, defined a scene-list listId to use to track scenes selected for bulk ordering.
    :param orderListName:
        String. Optional.   If provided, defined a scene-list listId to use to track scenes selected for on-demand ordering.
    :param excludeListName:
        String. Optional.   If provided, defined a scene-list listId to use to exclude scenes from the results.
    """
    payload = {
        "entityId": entityId,
        "datasetName": datasetName
    }
    if maxResults:
        payload["maxResults"] = maxResults
    if startingNumber:
        payload["startingNumber"] = startingNumber
    if metadataType:
        payload["metadataType"] = metadataType
    if sortField:
        payload["sortField"] = sortField
    if sortDirection:
        payload["sortDirection"] = sortDirection
    if compareListName:
        payload["compareListName"] = compareListName
    if bulkListName:
        payload["bulkListName"] = bulkListName
    if orderListName:
        payload["orderListName"] = orderListName
    if excludeListName:
        payload["excludeListName"] = excludeListName
    
    return payload

"""
def order_submit():
    pass

def ingest_subscription_create():
    pass

def download_request():
    pass

def download_options():
    pass

def tram_unit_update():
    pass

def user_set():
    pass
"""