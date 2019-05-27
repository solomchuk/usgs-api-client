"""
Author: Max Solomcuk, max.solomcuk@cgi.com

Data models for the USGS Inventory API.
See https://earthexplorer.usgs.gov/inventory/documentation/datamodel

TODO Make classes serialisable
"""

import json
from abc import ABC, abstractmethod
from datetime import date


class Bounds(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#Bounds
    """

    def __init__(self, north: float, east: float, south: float, west: float):
        if north > 90.0 or north < 0.0:
            raise ValueError('Invalid north latitude value: {}. Must be within [0, 90] bounds.'.format(north))
        if east > 180.0 or east < 0.0:
            raise ValueError('Invalid east longitude value: {}. Must be within [0, 180] bounds.'.format(east))
        if south > 0.0 or south < -90.0:
            raise ValueError('Invalid south latitude value: {}. Must be within [-90, 0] bounds.'.format(south))
        if west > 0.0 or west < -180.0:
            raise ValueError('Invalid west longitude value: {}. Must be within [-180, 0] bounds.'.format(west))
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'north': self.north,
            'east': self.east,
            'south': self.south,
            'west': self.west
        })

    def __str__(self):
        """
        Here and further - a shortcut for a string representation of a class. Will see if this needs changing.
        """
        return self.__repr__()

class BulkDownloadItemBasket(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#BulkDownloadItemBasket
    """

    def __init__(self, datasetName: str, bulkDownloadScenes: list):
        self.datasetName = datasetName
        self.bulkDownloadScenes = bulkDownloadScenes
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'datasetName': self.datasetName,
            'bulkDownloadScenes': self.bulkDownloadScenes
        })

    def __str__(self):
        return self.__repr__()

class BulkDownloadScene(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#BulkDownloadScene
    """

    def __init__(self, entityId: str, orderingId: str, products: list):
        self.entityId = entityId
        self.orderingId = orderingId
        self.products = products
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'entityId': self.entityId,
            'orderingId': self.orderingId,
            'products': self.products
        })

    def __str__(self):
        return self.__repr__()

class Coordinate(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#Coordinate
    """

    def __init__(self, latitude: float, longitude: float):
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError('Invalid latitude value: {}. Must be within [-90, 90] bounds.'.format(latitude))
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError('Invalid longitude value: {}. Must be within [-180, 180] bounds.'.format(longitude))
        self.latitude = latitude
        self.longitude = longitude
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'latitude': self.latitude,
            'longitude': self.longitude
        })

    def __str__(self):
        return self.__repr__()

class CriteriaField(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#CriteriaField
    """

    def __init__(self, fieldId: int, name: str, fieldLink: str, valueList: list):
        self.fieldId = fieldId
        self.name = name
        self.fieldLink = fieldLink
        self.valueList = valueList
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'fieldId': self.fieldId,
            'name': self.name,
            'fieldLink': self.fieldLink,
            'valueList': self.valueList
        })

    def __str__(self):
        return self.__repr__()

class DataAccess(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#DataAccess
    """

    def __init__(self, downloadUrl: str, orderUrl: str):
        self.downloadUrl = downloadUrl
        self.orderUrl = orderUrl
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'downloadUrl': self.downloadUrl,
            'orderUrl': self.orderUrl
        })

    def __str__(self):
        return self.__repr__()

class Dataset(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#Dataset
    """

    def __init__(self, bounds: Bounds, datasetName: str, datasetFullName: str, idnEntryId: str, startDate: date, endDate: date, lastModifiedDate: date,
                supportCloudCover: bool, supportDeletionInventory: bool, supportDownload: bool, supportBulkDownload: bool,
                bulkDownloadOrderLimit: int, supportOrder: bool, orderLimit: int, totalScenes: int):
        self.bounds = bounds
        self.datasetName = datasetName
        self.datasetFullName = datasetFullName
        self.idnEntryId = idnEntryId
        self.startDate = startDate
        self.endDate = endDate
        self.lastModifiedDate = lastModifiedDate
        self.supportCloudCover = supportCloudCover
        self.supportDeletionInventory = supportDeletionInventory
        self.supportDownload = supportDownload
        self.supportBulkDownload = supportBulkDownload
        self.bulkDownloadOrderLimit = bulkDownloadOrderLimit
        self.supportOrder = supportOrder
        self.orderLimit = orderLimit
        self.totalScenes = totalScenes
        super().__init__()

    def __repr__(self):
        return json.dumps({
        'bounds': self.bounds,
        'datasetName': self.datasetName,
        'datasetFullName': self.datasetFullName,
        'idnEntryId': self.idnEntryId,
        'startDate': self.startDate,
        'endDate': self.endDate,
        'lastModifiedDate': self.lastModifiedDate,
        'supportCloudCover': self.supportCloudCover,
        'supportDeletionInventory': self.supportDeletionInventory,
        'supportDownload': self.supportDownload,
        'supportBulkDownload': self.supportBulkDownload,
        'bulkDownloadOrderLimit': self.bulkDownloadOrderLimit,
        'supportOrder': self.supportOrder,
        'orderLimit': self.orderLimit,
        'totalScenes': self.totalScenes
        })

    def __str__(self):
        return self.__repr__()

class DeletedScene(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#DeletedScene
    """

    def __init__(self, acquisitionDate: date, entityId: str, displayId: str, deletionDate: date):
        self.acquisitionDate = acquisitionDate
        self.entityId = entityId
        self.displayId = displayId
        self.deletionDate = deletionDate
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'acquisitionDate': self.acquisitionDate,
            'entityId': self.entityId,
            'displayId': self.displayId,
            'deletionDate': self.deletionDate
        })

    def __str__(self):
        return self.__repr__()

class DeletionSearchResponse(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#DeletionSearchResponse
    """

    def __init__(self, numberReturned: int, totalHits: int, firstRecord: int, lastRecord: int, nextRecord: int, results: list):
        self.numberReturned = numberReturned
        self.totalHits = totalHits
        self.firstRecord = firstRecord
        self.lastRecord = lastRecord
        self.nextRecord = nextRecord
        self.results = results
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'numberReturned': self.numberReturned,
            'totalHits': self.totalHits,
            'firstRecord': self.firstRecord,
            'lastRecord': self.lastRecord,
            'nextRecord': self.nextRecord,
            'results': self.results
        })

    def __str__(self):
        return self.__repr__()

class DisplayListValue(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#DisplayListValue
    """

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'name': self.name,
            'value': self.value
        })

    def __str__(self):
        return self.__repr__()

class DownloadDetail(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#DownloadDetail
    """

    def __init__(self, filepath: str, storageLocation: str, returnData: bool):
        self.filepath = filepath
        self.storageLocation = storageLocation
        self.returnData = returnData
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'filepath': self.filepath,
            'storageLocation': self.storageLocation,
            'returnData': self.returnData
        })

    def __str__(self):
        return self.__repr__()

class DownloadLabel(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#DownloadLabel
    """

    def __init__(self, label: str, dateEntered: date, totalComplete: int, downloadCount: int, downloadSize: int):
        self.label = label
        self.dateEntered = dateEntered
        self.totalComplete = totalComplete
        self.downloadCount = downloadCount
        self.downloadSize = downloadSize
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'label': self.label,
            'dateEntered': self.dateEntered,
            'totalComplete': self.totalComplete,
            'downloadCount': self.downloadCount,
            'downloadSize': self.downloadSize
        })

    def __str__(self):
        return self.__repr__()

class DownloadRecord(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#DownloadRecord
    """

    def __init__(self, id: int, label: str, entityId: str, error: str, dataUse: str, datasetName: str, productCode: str, filesize: int, status: str, url: str):
        self.id = id
        self.label = label
        self.entityId = entityId
        self.error = error
        self.dataUse = dataUse
        self.datasetName = datasetName
        self.productCode = productCode
        self.filesize = filesize
        self.status = status
        self.url = url

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'label': self.label,
            'entityId': self.entityId,
            'error': self.error,
            'dataUse': self.dataUse,
            'datasetName': self.datasetName,
            'productCode': self.productCode,
            'filesize': self.filesize,
            'status': self.status,
            'url': self.url
        })

    def __str__(self):
        return self.__repr__()

class DownloadOption(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#DownloadOption
    """

    def __init__(self, available: bool, downloadCode: str, productCode: str, filesize: int, productName: str, url: str, storageLocation: str):
        self.available = available
        self.downloadCode = downloadCode
        self.productCode = productCode
        self.filesize = filesize
        self.productName = productName
        self.url = url
        self.storageLocation = storageLocation
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'available': self.available,
            'downloadCode': self.downloadCode,
            'productCode': self.productCode,
            'filesize': self.filesize,
            'productName': self.productName,
            'url': self.url,
            'storageLocation': self.storageLocation,
        })

    def __str__(self):
        return self.__repr__()

class DownloadQueue(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#DownloadQueue
    """

    def __init__(self, availableDownloads: list, failedRequests: list, requestedDownloads: list, queueSize: int):
        self.availableDownloads = availableDownloads
        self.failedRequests = failedRequests
        self.requestedDownloads = requestedDownloads
        self.queueSize = queueSize
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'availableDownloads': self.availableDownloads,
            'failedRequests': self.failedRequests,
            'requestedDownloads': self.requestedDownloads,
            'queueSize': self.queueSize
        })

    def __str__(self):
        return self.__repr__()

class ItemBasket(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#ItemBasket
    """

    def __init__(self, bulkDownloadItemBasket: list, orderItemBasket: list):
        self.bulkDownloadItemBasket = bulkDownloadItemBasket
        self.orderItemBasket = orderItemBasket
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'bulkDownloadItemBasket': self.bulkDownloadItemBasket,
            'orderItemBasket': self.orderItemBasket
        })

    def __str__(self):
        return self.__repr__()

class InventoryScene(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#InventoryScene
    """

    def __init__(self, acquisitionDate: date, startTime: date, endTime: date, lowerLeftCoordinate: Coordinate, upperLeftCoordinate: Coordinate, 
                upperRightCoordinate: Coordinate, lowerRightCoordinate: Coordinate, sceneBounds: str, browseUrl: str, dataAccessUrl: str, downloadUrl: str,
                entityId: str, displayId: str, metadataUrl: str, fgdcMetadataUrl: str, modifiedDate: date, orderUrl: str, summary: str):
        self.acquisitionDate = acquisitionDate
        self.startTime = startTime
        self.endTime = endTime
        self.lowerLeftCoordinate = lowerLeftCoordinate
        self.upperLeftCoordinate = upperLeftCoordinate
        self.upperRightCoordinate = upperRightCoordinate
        self.lowerRightCoordinate = lowerRightCoordinate
        self.sceneBounds = sceneBounds
        self.browseUrl = browseUrl
        self.dataAccessUrl = dataAccessUrl
        self.downloadUrl = downloadUrl
        self.entityId = entityId
        self.displayId = displayId
        self.metadataUrl = metadataUrl
        self.fgdcMetadataUrl = fgdcMetadataUrl
        self.modifiedDate = modifiedDate
        self.orderUrl = orderUrl
        self.summary = summary
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'acquisitionDate': self.acquisitionDate,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'lowerLeftCoordinate': self.lowerLeftCoordinate,
            'upperLeftCoordinate': self.upperLeftCoordinate,
            'upperRightCoordinate': self.upperRightCoordinate,
            'lowerRightCoordinate': self.lowerRightCoordinate,
            'sceneBounds': self.sceneBounds,
            'browseUrl': self.browseUrl,
            'dataAccessUrl': self.dataAccessUrl,
            'downloadUrl': self.downloadUrl,
            'entityId': self.entityId,
            'displayId': self.displayId,
            'metadataUrl': self.metadataUrl,
            'fgdcMetadataUrl': self.fgdcMetadataUrl,
            'modifiedDate': self.modifiedDate,
            'orderUrl': self.orderUrl,
            'summary': self.summary
        })

    def __str__(self):
        return self.__repr__()

class MetadataField(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#MetadataField
    """

    def __init__(self, fieldName: str, descriptionLink: str, value: str):
        self.fieldName = fieldName
        self.descriptionLink = descriptionLink
        self.value = value
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'fieldName': self.fieldName,
            'descriptionLink': self.descriptionLink,
            'value': self.value
        })

    def __str__(self):
        return self.__repr__()

class Notification(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#Notification
    """

    def __init__(self, message: str, severity: str, title: str):
        self.message = message
        self.severity = severity
        self.title = title
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'message': self.message,
            'severity': self.severity,
            'title': self.title
        })

    def __str__(self):
        return self.__repr__()

class OrderDataset(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#OrderDataset
    """

    def __init__(self, datasetName: str, products: list):
        self.datasetName = datasetName
        self.products = products
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'datasetName': self.datasetName,
            'products': self.products
        })

    def __str__(self):
        return self.__repr__()

class OrderDatasetProduct(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#OrderDatasetProduct
    """

    def __init__(self, option: str, outputMedia: str, productCode: str, entityIds: list):
        self.option = option
        self.outputMedia = outputMedia
        self.productCode = productCode
        self.entityIds = entityIds
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'option': self.option,
            'outputMedia': self.outputMedia,
            'productCode': self.productCode,
            'entityIds': self.entityIds
        })

    def __str__(self):
        return self.__repr__()

class OrderItemBasket(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#OrderItemBasket
    """

    def __init__(self, datasetName: str, orderScenes: list):
        self.datasetName = datasetName
        self.orderScenes = orderScenes
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'datasetName': self.datasetName,
            'orderScenes': self.orderScenes
        })

    def __str__(self):
        return self.__repr__()

class OrderProduct(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#OrderProduct
    """

    def __init__(self, option: str, originator: str, outputMedia: str, price: float, productCode: str, productName: str):
        self.option = option
        self.originator = originator
        self.outputMedia = outputMedia
        self.price = price
        self.productCode = productCode
        self.productName = productName
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'option': self.option,
            'originator': self.originator,
            'outputMedia': self.outputMedia,
            'price': self.price,
            'productCode': self.productCode,
            'productName': self.productName
        })

    def __str__(self):
        return self.__repr__()

class OrderProductOption(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#OrderProductOption
    """

    def __init__(self, options: list, outputMedias: list, price: float, productCode: str, productName: str):
        self.options = options
        self.outputMedias = outputMedias
        self.price = price
        self.productCode = productCode
        self.productName = productName
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'options': self.options,
            'outputMedias': self.outputMedias,
            'price': self.price,
            'productCode': self.productCode,
            'productName': self.productName
        })

    def __str__(self):
        return self.__repr__()

class OrderScene(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#OrderScene
    """

    def __init__(self, entityId: str, orderingId: str, availableProducts: list, product: OrderProduct):
        self.entityId = entityId
        self.orderingId = orderingId
        self.availableProducts = availableProducts
        self.product = product
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'entityId': self.entityId,
            'orderingId': self.orderingId,
            'availableProducts': self.availableProducts,
            'product': self.product
        })

    def __str__(self):
        return self.__repr__()

class OrderStatus(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#OrderStatus
    """

    def __init__(self, orderNumber: str, statusCode: str, statusText: str, units: list):
        self.orderNumber = orderNumber
        self.statusCode = statusCode
        self.statusText = statusText
        self.units = units
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'orderNumber': self.orderNumber,
            'statusCode': self.statusCode,
            'statusText': self.statusText,
            'units': self.units
        })

    def __str__(self):
        return self.__repr__()

class OrderUnitStatus(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#OrderUnitStatus
    """

    def __init__(self, datasetName: str, displayId: str, entityId: str, orderingId: str, productCode: str, productDescription: str, statusCode: str,
                statusText: str, unitNumber: str):
        self.datasetName = datasetName
        self.displayId = displayId
        self.entityId = entityId
        self.orderingId = orderingId
        self.productCode = productCode
        self.productDescription = productDescription
        self.statusCode = statusCode
        self.statusText = statusText
        self.unitNumber = unitNumber
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'datasetName': self.datasetName,
            'displayId': self.displayId,
            'entityId': self.entityId,
            'orderingId': self.orderingId,
            'productCode': self.productCode,
            'productDescription': self.productDescription,
            'statusCode': self.statusCode,
            'statusText': self.statusText,
            'unitNumber': self.unitNumber
        })

    def __str__(self):
        return self.__repr__()

class Scene(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#Scene
    """

    def __init__(self, acquisitionDate: date, startTime: date, endTime: date, spatialFootprint: str, sceneBounds: str, browseUrl: str, dataAccessUrl: str,
                downloadUrl: str, entityId: str, displayId: str, metadataUrl: str, fgdcMetadataUrl: str, modifiedDate: date, orderUrl: str, summary: str):
        self.acquisitionDate = acquisitionDate
        self.startTime = startTime
        self.endTime = endTime
        self.spatialFootprint = spatialFootprint
        self.sceneBounds = sceneBounds
        self.browseUrl = browseUrl
        self.dataAccessUrl = dataAccessUrl
        self.downloadUrl = downloadUrl
        self.entityId = entityId
        self.displayId = displayId
        self.metadataUrl = metadataUrl
        self.fgdcMetadataUrl = fgdcMetadataUrl
        self.modifiedDate = modifiedDate
        self.orderUrl = orderUrl
        self.summary = summary
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'acquisitionDate': self.acquisitionDate,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'spatialFootprint': self.spatialFootprint,
            'sceneBounds': self.sceneBounds,
            'browseUrl': self.browseUrl,
            'dataAccessUrl': self.dataAccessUrl,
            'downloadUrl': self.downloadUrl,
            'entityId': self.entityId,
            'displayId': self.displayId,
            'metadataUrl': self.metadataUrl,
            'fgdcMetadataUrl': self.fgdcMetadataUrl,
            'modifiedDate': self.modifiedDate,
            'orderUrl': self.orderUrl,
            'summary': self.summary,
        })

    def __str__(self):
        return self.__repr__()

class SceneDownloadOptions(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#SceneDownloadOptions
    """

    def __init__(self, downloadOptions: list, entityId: str):
        self.downloadOptions = downloadOptions
        self.entityId = entityId
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'downloadOptions': self.downloadOptions,
            'entityId': self.entityId
        })

    def __str__(self):
        return self.__repr__()

class SearchFilter(ABC):
    """
    This is an abstract data model, use SearchFilterAnd, SearchFilterBetween, SearchFilterOr, or SearchFilterValue
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#SearchFilter
    """

    def __init__(self, filterType):
        self.filterType = filterType
        super().__init__()

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

class SearchFilterAnd(SearchFilter):
    """
    An "and" search filter data structure.
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#SearchFilterAnd
    """

    def __init__(self, filterType='and', childFilters=[]):
        self.childFilters = childFilters
        super().__init__(filterType)

    def __repr__(self):
        return json.dumps({
            'filterType': self.filterType,
            'childFilters': self.childFilters
        })

    def __str__(self):
        return self.__repr__()

class SearchFilterBetween(SearchFilter):
    """
    A "between" search filter data structure.
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#SearchFilterBetween
    """

    def __init__(self, fieldId: int, firstValue: str, secondValue: str, filterType='between'):
        self.fieldId = fieldId
        self.firstValue = firstValue
        self.secondValue = secondValue
        super().__init__(filterType)

    def __repr__(self):
        return json.dumps({
            'filterType': self.filterType,
            'fieldId': self.fieldId,
            'firstValue': self.firstValue,
            'secondValue': self.secondValue
        })

    def __str__(self):
        return self.__repr__()

class SearchFilterOr(SearchFilter):
    """
    An "or" search filter data structure.
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#SearchFilterOr
    """

    def __init__(self, filterType='or', childFilters=[]):
        self.childFilters = childFilters
        super().__init__(filterType)

    def __repr__(self):
        return json.dumps({
            'filterType': self.filterType,
            'childFilters': self.childFilters
        })

    def __str__(self):
        return self.__repr__()

class SearchFilterValue(SearchFilter):
    """
    A "value" search filter data structure.
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#SearchFilterValue
    """

    def __init__(self, fieldId: int, value: str, operand: str, filterType='value'):
        self.fieldId = fieldId
        self.value = value
        if operand in ['=', 'like']:
            self.operand = operand
        else:
            self.operand = '='
        super().__init__(filterType)

    def __repr__(self):
        return json.dumps({
            'filterType': self.filterType,
            'fieldId': self.fieldId,
            'value': self.value,
            'operand': self.operand
        })

    def __str__(self):
        return self.__repr__()

class SceneMetadata(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#SceneMetadata
    """

    def __init__(self, acquisitionDate: date, startTime: date, endTime: date, spatialFootprint: str, sceneBounds: str, browseUrl: str, dataAccess: DataAccess,
                dataAccessUrl: str, downloadUrl: str, entityId: str, displayId: str, metadataUrl: str, fgdcMetadataUrl: str, modifiedDate: date, orderUrl: str,
                summary: str, metadataFields: list):
        self.acquisitionDate = acquisitionDate
        self.startTime = startTime
        self.endTime = endTime
        self.spatialFootprint = spatialFootprint
        self.sceneBounds = sceneBounds
        self.browseUrl = browseUrl
        self.dataAccess = dataAccess
        self.dataAccessUrl = dataAccessUrl
        self.downloadUrl = downloadUrl
        self.entityId = entityId
        self.displayId = displayId
        self.metadataUrl = metadataUrl
        self.fgdcMetadataUrl = fgdcMetadataUrl
        self.modifiedDate = modifiedDate
        self.orderUrl = orderUrl
        self.summary = summary
        self.metadataFields = metadataFields
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'acquisitionDate': self.acquisitionDate,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'spatialFootprint': self.spatialFootprint,
            'sceneBounds': self.sceneBounds,
            'browseUrl': self.browseUrl,
            'dataAccess': self.dataAccess,
            'dataAccessUrl': self.dataAccessUrl,
            'downloadUrl': self.downloadUrl,
            'entityId': self.entityId,
            'displayId': self.displayId,
            'metadataUrl': self.metadataUrl,
            'fgdcMetadataUrl': self.fgdcMetadataUrl,
            'modifiedDate': self.modifiedDate,
            'orderUrl': self.orderUrl,
            'summary': self.summary,
            'metadataFields': self.metadataFields
        })

    def __str__(self):
        return self.__repr__()

class SearchResponse(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#SearchResponse
    """

    def __init__(self, numberReturned: int, totalHits: int, firstRecord: int, lastRecord: int, nextRecord: int, results: list):
        self.numberReturned = numberReturned
        self.totalHits = totalHits
        self.firstRecord = firstRecord
        self.lastRecord = lastRecord
        self.nextRecord = nextRecord
        self.results = results
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'numberReturned': self.numberReturned,
            'totalHits': self.totalHits,
            'firstRecord': self.firstRecord,
            'lastRecord': self.lastRecord,
            'nextRecord': self.nextRecord,
            'results': self.results
        })

    def __str__(self):
        return self.__repr__()

class SpatialFilter(ABC):
    """
    This is an abstract data model, use SpatialFilterMbr
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#SpatialFilter
    """

    def __init__(self, filterType):
        self.filterType = filterType
        super().__init__()
    
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

class SpatialFilterMbr(SpatialFilter):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#SpatialFilterMbr
    """

    def __init__(self, lowerLeft: Coordinate, upperRight: Coordinate, filterType='mbr'):
        self.lowerLeft = lowerLeft
        self.upperRight = upperRight
        super().__init__(filterType)

    def __repr__(self):
        return json.dumps({
            'filterType': self.filterType,
            'lowerLeft': self.lowerLeft,
            'upperRight': self.upperRight
        })

    def __str__(self):
        return self.__repr__()

class Status(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#Status
    """

    def __init__(self, build_date: str):
        self.build_date = build_date
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'build_date': self.build_date,
        })

    def __str__(self):
        return self.__repr__()

class TemporalFilter(object):
    """
    https://earthexplorer.usgs.gov/inventory/documentation/datamodel#TemporalFilter
    """

    def __init__(self, startDate: date, endDate: date):
        self.startDate = startDate
        self.endDate = endDate
        super().__init__()

    def __repr__(self):
        return json.dumps({
            'startDate': self.startDate,
            'endDate': self.endDate
        })

    def __str__(self):
        return self.__repr__()
