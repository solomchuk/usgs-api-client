#!/usr/bin/env python

"""
Author: Max Solomcuk, max.solomcuk@cgi.com

Data types for the USGS Inventory API.
See https://m2m.cr.usgs.gov/api/docs/datatypes/

TODO Make classes serialisable
"""

from abc import ABC, abstractmethod
#from datetime import date

class AcquisitionFilter(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#acquisitionFilter
    """
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end
        super().__init__()

    def __repr__(self):
        return {
            "start": self.start,
            "end": self.end
        }
    
    def __str__(self):
        return str(self.__repr__())

class CloudCoverFilter(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#cloudCoverFilter
    """
    def __init__(self, min: int, max: int, includeUnknown: bool):
        self.min = min
        self.max = max
        self.includeUnknown = includeUnknown
        super().__init__()

    def __repr__(self):
        return {
            "min": self.min,
            "max": self.max,
            "includeUnknown": self.includeUnknown
        }

    def __str__(self):
        return str(self.__repr__())

class Coordinate(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#coordinate
    """

    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude
        super().__init__()

    def __repr__(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    def __str__(self):
        return str(self.__repr__())

class DateRange(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#dateRange
    """
    def __init__(self, startDate: str, endDate: str):
        self.startDate = startDate
        self.endDate = endDate
        super().__init__()
    
    def __repr__(self):
        return {
            "startDate": self.startDate,
            "endDate": self.endDate
        }
    
    def __str__(self):
        return str(self.__repr__())

class GeoJson(SpatialBounds):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#geoJson
    """
    def __init__(self, type: str, coordinates: list):
        self.type = type
        self.coordinates = coordiantes
        super().__init__()

    def __repr__(self):
        return {
            "type": self.type,
            "coordinates": self.coordinates
        }
    
    def __str__(self):
        return str(self.__repr__())

class IngestFilter(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#ingestFilter
    """
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end
        super().__init__()

    def __repr__(self):
        return {
            "start": self.start,
            "end": self.end
        }

    def __str__(self):
        return str(self.__repr__())

class MetadataFilter(ABC):
    """
    This is an abstract data model, use MetadataAnd, MetadataBetween, MetadataOr, or MetadataValue.
    https://m2m.cr.usgs.gov/api/docs/datatypes/#metadataFilter
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

class MetadataAnd(MetadataFilter):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#metadataAnd
    """
    def __init__(self, filterType="and", childFilters: list):
        self.filterType = filterType
        self.childFilters = childFilters
        super().__init__(filterType)

    def __repr__(self):
        return {
            "filterType": self.filterType,
            "childFilters": self.childFilters
        }
    
    def __str__(self):
        return str(self.__repr__())

class MetadataBetween(MetadataFilter):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#metadataBetween
    """
    def __init__(self, filterType="between", filterId: str, firstValue: int, secondValue: int):
        self.filterType = filterType
        self.filterId = filterId
        self.firstValue = firstValue
        self.secondValue = secondValue
        super().__init__(filterType)

    def __repr__(self):
        return {
            "filterType": self.filterType,
            "filterId": self.filterId,
            "firstValue": self.firstValue,
            "secondValue": self.secondValue
        }
    
    def __str__(self):
        return str(self.__repr__())

class MetadataOr(MetadataFilter):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#metadataOr
    """
    def __init__(self, filterType="or", childFilters: list):
        self.filterType = filterType
        self.childFilters = childFilters
        super().__init__(filterType)

    def __repr__(self):
        return {
            "filterType": self.filterType,
            "childFilters": self.childFilters
        }
    
    def __str__(self):
        return str(self.__repr__())

class MetadataValue(MetadataFilter):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#metadataValue
    """
    def __init__(self, filterType="value", filterId: str, value: str, operand: str):
        self.filterType = filterType
        self.filterId = filterId
        self.value = value
        self.operand = operand
        super().__init__(filterType)

    def __repr__(self):
        return {
            "filterType": self.filterType,
            "filterId": self.filterId,
            "value": self.value,
            "operand": self.operand
        }
    
    def __str__(self):
        return str(self.__repr__())

class SceneFilter(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#sceneFilter
    """
    def __init__(self, acquisitionFilter: AcquisitionFilter, cloudCoverFilter: CloudCoverFilter,
                datasetName: str, ingestFilter: IngestFilter, metadataFilter: MetadataFilter,
                seasonalFilter: list, spatialFilter: SpatialFilter):
        self.acquisitionFilter = acquisitionFilter
        self.cloudCoverFilter = cloudCoverFilter
        self.datasetName = datasetName
        self.ingestFilter = ingestFilter
        self.metadataFilter = metadataFilter
        self.seasonalFilter = seasonalFilter
        self.spatialFilter = spatialFilter
        super().__init__()
    
    def __repr__(self):
        return {
            "acquisitionFilter": self.acquisitionFilter,
            "cloudCoverFilter": self.cloudCoverFilter,
            "datsetName": self.datasetName,
            "ingestFilter": self.ingestFilter,
            "metadataFilter": self.metadataFilter,
            "seasonalFilter": self.seasonalFilter,
            "spatialFilter": self.spatialFilter
        }
    
    def __str__(self):
        return str(self.__repr__())

class SpatialBounds(ABC):
    """
    This is an abstract data model, use spatialBoundsMbr or geoJson.
    https://m2m.cr.usgs.gov/api/docs/datatypes/#spatialBounds
    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass    

class SpatialBoundsMbr(SpatialBounds):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#spatialBoundsMbr
    """
    def __init__(self, north: str, east: str, south: str, west: str):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        super().__init__()

    def __repr__(self):
        return {
            "north": self.north,
            "east": self.east,
            "south": self.south,
            "west": self.west
        }

    def __str__(self):
        return str(self.__repr__())

class SpatialFilter(ABC):
    """
    This is an abstract data model, use SpatialFilterMbr or SpatialFilterGeoJson.
    https://m2m.cr.usgs.gov/api/docs/datatypes/#spatialFilter
    """
    def __init__(self, filterType: str):
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
    https://m2m.cr.usgs.gov/api/docs/datatypes/#spatialFilterMbr
    """
    def __init__(self, filterType="mbr", lowerLeft: Coordinate, upperRight: Coordinate):
        self.filterType = filterType
        self.lowerLeft = lowerLeft
        self.upperRight = upperRight
        super().__init__(filterType)

    def __repr__(self):
        return {
            "filterType": self.filterType,
            "lowerLeft": self.lowerLeft,
            "upperRight": self.upperRight
        }

    def __str__(self):
        return str(self.__repr__())

class SpatialFilterGeoJson(SpatialFilter):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#spatialFilterGeoJson
    """
    def __init__(self, filterType="geoJson", geoJson: GeoJson):
        self.filterType = filterType
        self.geoJson = geoJson
        super().__init__(filterType)

    def __repr__(self):
        return {
            "filterType": self.filterType,
            "geoJson": self.geoJson
        }

    def __str__(self):
        return str(self.__repr__())

class UserContext(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#userContext
    """
    def __init__(self, contactId: str, ipAddress: str):
        self.contactId = contactId
        self.ipAddress = ipAddress
        super().__init__()

    def __repr__(self):
        return {
            "contactId": self.contactId,
            "ipAddress": self.ipAddress
        }
    
    def __str__(self):
        return str(self.__repr__())

class TemporalCoverage(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#temporalCoverage
    NOTE: both inputs are listed as ISO 8601 "date" type, check if API uses strings instead.
    """
    def __init__(self, startDate: str, endDate: str):
        self.startDate = startDate
        self.endDate = endDate
        super().__init__()

    def __repr__(self):
        return {
            "startDate": self.startDate,
            "endDate": self.endDate
        }
    
    def __str__(self):
        return str(self.__repr__())

class TemporalFilter(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#temporalFilter
    NOTE: both inputs are listed as ISO 8601 "date" type, check if API uses strings instead.
    """
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end
        super().__init__()

    def __repr__(self):
        return {
            "start": self.start,
            "end": self.end
        }
    
    def __str__(self):
        return str(self.__repr__())

class DownloadResponse(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#download
    NOTE: secondaryDownloads is an array of DownloadResponse objects.
    """
    def __init__(self, id: int, displayId: str, entityId: str, datasetId: str, available: str,
                filesize: int, productName: str, productCode: str, bulkAvailable: str,
                downloadSystem: str, secondaryDownloads: list):
        self.id = id
        self.displayId = displayId
        self.entityId = entityId
        self.datasetId = datasetId
        self.available = available
        self.filesize = filesize
        self.productName = productName
        self.bulkAvailable = bulkAvailable
        self.downloadSystem = downloadSystem
        self.secondaryDownloads = secondaryDownloads
        super().__init__()

    def __repr__(self):
        return {
            "id": self.id,
            "displayId": self.displayId,
            "entityId": self.entityId,
            "datasetId": self.datasetId,
            "available": self.available,
            "filesize": self.filesize,
            "productName": self.productName,
            "bulkAvailable": self.bulkAvailable,
            "downloadSystem": self.downloadSystem,
            "secondaryDonwloads": self.secondaryDownloads
        }

    def __str__(self):
        return str(self.__repr__())

class DownloadInput(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#download[]
    """
    def __init__(self, entityId: str, productId: str, dataUse: str, label: str):
        self.entityId = entityId
        self.productId = productId
        self.dataUse = dataUse
        self.label = label
        super().__init__()

    def __repr__(self):
        return {
            "entityId": self.entityId,
            "productId": self.productId,
            "dataUse": self.dataUse,
            "label": self.label
        }

    def __str__(self):
        return str(self.__repr__())

class DownloadQueueDownload(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#downloadQueueDownload
    """
    def __init__(self, downloadId: int, collectionName: str, datasetId: str, displayId: str,
                entityId: str, eulaCode: str, filesize: int, label: str, productCode: str,
                productName: str, statusCode: str, statusText: str):
        self.downloadId = downloadId
        self.collectionName = collectionName
        self.datasetId = datasetId
        self.displayId = displayId
        self.entityId = entityId
        self.eulaCode = eulaCode
        self.filesize = filesize
        self.label = label
        self.productCode = productCode
        self.productName = productName
        self.statusCode = statusCode
        self.statusText = statusText
        super().__init__()

    def __repr__(self):
        return {
            "downloadId": self.downloadId,
            "collectionName": self.collectionName,
            "datasetId": self.datasetId,
            "displayId": self.displayId,
            "entityId": self.entityId,
            "eulaCode": self.eulaCode,
            "filesize": self.filesize,
            "label": self.label,
            "productCode": self.productCode,
            "productName": self.productName,
            "statusCode": self.statusCode,
            "statusText": self.statusText
        }
    
    def __str__(self):
        return str(self.__repr__())

class Eula(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#eula
    """
    def __init__(self, eulaCode: str, agreementContent: str):
        self.eulaCode = eulaCode
        self.agreementContent = agreementContent
        super().__init__()

    def __repr__(self):
        return {
            "eulaCode": self.eulaCode,
            "agreementContent": self.agreementContent
        }

    def __str__(self):
        return str(self.__repr__())

class FilepathDownload(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#filepathDownload[]
    """
    def __init__(self, datasetName: str, productCode: str, dataPath: str, dataUse: str, label: str):
        self.datasetName = datasetName
        self.productCode = productCode
        self.dataPath = dataPath
        self.dataUse = dataUse
        self.label = label
        super().__init__()

    def __repr__(self):
        return {
            "datasetName": self.datasetName,
            "productCode": self.productCode,
            "dataPath": self.dataPath,
            "dataUse": self.dataUse,
            "label": self.label
        }

    def __str__(self):
        return str(self.__repr__())

class Options(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#options
    """
    def __init__(self, bulk: bool, order: bool, download: bool, secondary: bool):
        self.bulk = bulk
        self.order = order
        self.download = download
        self.secondary = secondary
        super().__init__()

    def __repr__(self):
        return {
            "bulk": self.bulk,
            "order": self.order,
            "download": self.download,
            "secondary": self.secondary
        }

    def __str__(self):
        return str(self.__repr__())

class ProductDownload(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#productDownload[]
    """
    def __init__(self, datasetName: str, productIds: list, sceneFilter: SceneFilter):
        self.datasetName = datasetName
        self.productIds = productIds
        self.sceneFilter = sceneFilter
        super().__init__()

    def __repr__(self):
        return {
            "datasetName": self.datasetName,
            "productIds": self.productIds,
            "sceneFilter": self.sceneFilter
        }
    
    def __str__(self):
        return str(self.__repr__())

class Selected(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#selected
    """
    def __init__(self, bulk: bool, order: bool, compare: bool):
        self.bulk = bulk
        self.order = order
        self.compare = compare
        super().__init__()

    def __repr__(self):
        return {
            "bulk": self.bulk,
            "order": self.order,
            "compare": self.compare
        }
    
    def __str__(self):
        return str(self.__repr__())
    
class MetadataExport(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#metadataExport
    """
    def __init__(self, exportId: str, exportName: str, datasetId: str, datasetName: str,
                sceneFilter: SceneFilter, customMessage: str, exportType: str, status: str,
                statusName: str, dateEntered: str, dateUpdated: str):
        self.exportId = exportId
        self.exportName = exportName
        self.datasetId = datasetId
        self.datasetName = datasetName
        self.sceneFilter = sceneFilter
        self.customMessage = customMessage
        self.exportType = exportType
        self.status = status
        self.statusName = statusName
        self.dateEntered = dateEntered
        self.dateUpdated = dateUpdated
        super().__init__()

    def __repr__(self):
        return {
            "exportId": self.exportId,
            "exportName": self.exportName,
            "datasetId": self.datasetId,
            "datasetName": self.datasetName,
            "sceneFilter": self.sceneFilter,
            "customMessage": self.customMessage,
            "exportType": self.exportType,
            "status": self.status,
            "statusName": self.statusName,
            "dateEntered": self.dateEntered,
            "dateUpdated": self.dateUpdated
        }

    def __str__(self):
        return str(self.__repr__())

class MetadataField(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#metadataField
    """
    def __init__(self, id: int, fieldName: str, dictionaryLink: str, value: str):
        self.id = id
        self.fieldName = fieldName
        self.dictionaryLink = dictionaryLink
        self.value = value
        super().__init__()

    def __repr__(self):
        return {
            "id": self.id,
            "fieldName": self.fieldName,
            "dictionaryLink": self.dictionaryLink,
            "value": self.value
        }

    def __str__(self):
        return str(self.__repr__())

class Browse(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#browse
    """
    def __init__(self, browseRotationEnabled: bool, browseName: str, browsePath: str,
                overlayPath: str, overlayType: str, thumbnailPath: str):
        self.browseRotationEnabled = browseRotationEnabled
        self.browseName = browseName
        self.browsePath = browsePath
        self.overlayPath = overlayPath
        self.overlayType = overlayType
        self.thumbnailPath = thumbnailPath
        super().__init__()

    def __repr__(self):
        return {
            "browseRotationEnabled": self.browseRotationEnabled,
            "browseName": self.browseName,
            "browsePath": self.browsePath,
            "overlayPath": self.overlayPath,
            "overlayType": self.overlayType,
            "thumbnailPath": self.thumbnailPath
        }

    def __str__(self):
        return str(self.__repr__())

class Dataset(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#dataset
    """
    def __init__(self, abstractText: str, acquisitionStart: str, acquisitionEnd: str,
                catalogs: list, collectionName: str, collectionLongName: str, datasetId: str,
                datasetAlias: str, datasetCategoryName: str, dataOwner: str, dateUpdated: str,
                doiNumber: str, ingestFrequency: str, keywords: str, sceneCount: int,
                spatialBounds: SpatialBounds, temporalCoverage: TemporalCoverage,
                supportCloudCover: bool, supportDeletionSearch: bool):
        self.abstractText = abstractText
        self.acquisitionStart = acquisitionStart
        self.acquisitionEnd = acquisitionEnd
        self.catalogs = catalogs
        self.collectionName = collectionName
        self.collectionLongName = collectionLongName
        self.datasetId = datasetId
        self.datasetAlias = datasetAlias
        self.datasetCategoryName = datasetCategoryName
        self.dataOwner = dataOwner
        self.dateUpdated = dateUpdated
        self.doiNumber = doiNumber
        self.ingestFrequency = ingestFrequency
        self.keywords = keywords
        self.sceneCount = sceneCount
        self.spatialBounds = spatialBounds
        self.temporalCoverage = temporalCoverage
        self.supportCloudCover = supportCloudCover
        self.supportDeletionSearch = supportDeletionSearch
        super().__init__()

    def __repr__(self):
        return {
            "abstractText": self.abstractText,
            "acquisitionStart": self.acquisitionStart
            "acquisitionEnd": self.acquisitionEnd,
            "catalogs": self.catalogs,
            "collectionName": self.collectionName,
            "collectionLongName": self.collectionLongName,
            "datasetId": self.datasetId,
            "datasetAlias": self.datasetAlias,
            "datasetCategoryName": self.datasetCategoryName,
            "dataOwner": self.dataOwner,
            "dateUpdated": self.dateUpdated,
            "doiNumber": self.doiNumber,
            "ingestFrequency": self.ingestFrequency,
            "keywords": self.keywords,
            "sceneCount": self.sceneCount,
            "spatialBounds": self.spatialBounds,
            "temporalCoverage": self.temporalCoverage,
            "supportCloudCover": self.supportCloudCover,
            "supportDeletionSearch": self.supportDeletionSearch
        }

    def __str__(self):
        return str(self.__repr__())

class DatasetCategory(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#datasetCategory
    """
    def __init__(self, id: int, categoryName: str, categoryDescription: str, parentCategoryId: int,
                parentCategoryName: str, referenceLink: str):
        self.id = id
        self.categoryName = categoryName
        self.categoryDescription = categoryDescription
        self.parentCategoryId = parentCategoryId
        self.parentCategoryName = parentCategoryName
        self.referenceLink = referenceLink
        super().__init__()

    def __repr__(self):
        return {
            "id": self.id,
            "categoryName": self.categoryName,
            "categoryDescription": self.categoryDescription,
            "parentCategoryId": self.parentCategoryId,
            "parentCategoryName": self.parentCategoryName,
            "referenceLink": self.referenceLink
        }

    def __str__(self):
        return str(self.__repr__())

class DatasetFilter(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#datasetFilter
    """
    def __init__(self, id: int, legacyFieldId: int, dictionaryLink: str, fieldConfig: FieldConfig,
                fieldLabel: str, searchSql: str):
        self.id = id
        self.legacyFieldId = legacyFieldId
        self.dictionaryLink = dictionaryLink
        self.fieldConfig = fieldConfig
        self.fieldLabel = fieldLabel
        self.searchSql = searchSql
        super().__init__()

    def __repr__(self):
        return {
            "id": self.id,
            "legacyFieldId": self.legacyFieldId,
            "dictionaryLink": self.dictionaryLink,
            "fieldConfig": self.fieldConfig,
            "fieldLabel": self.fieldLabel,
            "searchSql": self.searchSql
        }

    def __str__(self):
        return str(self.__repr__())

class FieldConfig(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#fieldConfig
    """
    def __init__(self, type: str, filters: list, validators: list, displayListId: str):
        self.type = type
        self.filters = filters
        self.validators = validators
        self.displayListId = displayListId
        super().__init__()

    def __repr__(self):
        return {
            "type": self.type,
            "filters": self.filters,
            "validators": self.validators,
            "displayListId": self.displayListId
        }

    def __str__(self):
        return str(self.__repr__())

class Notification(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#notification
    """
    def __init__(self, id: int, subject: str, messageContent: str, severityCode: str,
                severityCssClass: str, severityText: str, dateUpdated: str):
        self.id = id
        self.subject = subject
        self.messageContent = messageContent
        self.severityCode = severityCode
        self.severityCssClass = severityCssClass
        self.severityText = severityText
        self.dateUpdated = dateUpdated
        super().__init__()

    def __repr__(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "messageContent": self.messageContent,
            "severityCode": self.severityCode,
            "severityCssClass": self.severityCssClass,
            "severityText": self.severityText,
            "dateUpdated": self.dateUpdated
        }

    def __str__(self):
        return str(self.__repr__())

class ProductResponse(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#product
    """
    def __init__(self, id: int, entityId: str, datasetId: str, available: str, price: float,
                productName: str, productCode: str):
        self.id = id
        self.entityId = entityId
        self.datasetId = datasetId
        self.available = available
        self.price = price
        self.productName = productName
        self.productCode = productCode
        super().__init__()

    def __repr__(self):
        return {
            "id": self.id,
            "entityId": self.entityId,
            "datasetId": self.datasetId,
            "available": self.available,
            "price": self.price,
            "productName": self.productName,
            "productCode": self.productCode
        }

    def __str__(self):
        return str(self.__repr__())

class ProductInput(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#product[]
    """
    def __init__(self, datasetName: str, entityId: str, productId: str, productCode: str):
        self.datasetName = datasetName
        self.entityId = entityId
        self.productId = productId
        self.productCode = productCode
        super().__init__()

    def __repr__(self):
        return {
            "datasetName": self.datasetName,
            "entityId": self.entityId,
            "productId": self.productId,
            "productCode": self.productCode
        }

    def __str__(self):
        return str(self.__repr__())

class RunOptions(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#runOptions
    """
    def __init__(self, resultFormats: list):
        self.resultFormats = resultFormats
        super().__init__()

    def __repr__(self):
        return {
            "resultFormats": self.resultFormats
        }

    def __str__(self):
        return str(self.__repr__())

class Scene(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#scene
    """
    def __init__(self, browse: Browse, cloudCover: str, entityId: str, displayId: str,
                metadata: list, options: Options, selected: Selected, spatialBounds: SpatialBounds,
                spatialCoverage: SpatialBounds, temporalCoverage: TemporalCoverage, publishDate: str):
        self.browse = browse
        self.cloudCover = cloudCover
        self.entityId = entityId
        self.displayId = displayId
        self.metadata = metadata
        self.options = options
        self.selected = selected
        self.spatialBounds = spatialBounds
        self.spatialCoverage = spatialCoverage
        self.temporalCoverage = temporalCoverage
        self.publishDate = publishDate
        super().__init__()

    def __repr__(self):
        return {
            "browse": self.browse,
            "cloudCover": self.cloudCover,
            "entityId": self.entityId,
            "displayId": self.displayId,
            "metadata": self.metadata,
            "options": self.options,
            "selected": self.selected,
            "spatialBounds": self.spatialBounds,
            "spatialCoverage": self.spatialCoverage,
            "temporalCoverage": self.temporalCoverage,
            "publishDate": self.publishDate
        }

    def __str__(self):
        return str(self.__repr__())

class IngestSubscription(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#ingestSubscription
    """
    def __init__(self, subscriptionId: int, subscriptionName: str, username: str, catalogId: str,
                datasets: str, runOptions: RunOptions, runStartDate: str, runEndDate: str,
                requestApp: str, requestAppReferenceId: str, runFrequency: str, status: str,
                dateEntered: str, lastRunDate: str, lastAttemptDate: str):
        self.subscriptionId = subscriptionId
        self.subscriptionName = subscriptionName
        self.username = username
        self.catalogId = catalogId
        self.requestApp = requestApp
        self.requestAppReferenceId = requestAppReferenceId
        self.runFrequency = runFrequency
        self.status = status
        self.dateEntered = dateEntered
        self.lastRunDate = lastRunDate
        self.lastAttemptDate = lastAttemptDate
        super().__init__()

    def __repr__(self):
        return {
            "subscriptionId": self.subscriptionId,
            "subscriptionName": self.subscriptionName,
            "username": self.username,
            "catalogId": self.catalogId,
            "requestApp": self.requestApp,
            "requestAppReferenceId": self.requestAppReferenceId,
            "runFrequency": self.runFrequency,
            "status": self.status,
            "dateEntered": self.dateEntered,
            "lastRunDate": self.lastRunDate,
            "lastAttemptDate": self.lastAttemptDate
        }

    def __str__(self):
        return str(self.__repr__())

class IngestSubscriptionLog(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#IngestSubscriptionLog
    """
    def __init__(self, runId: int, subscriptionId: int, runDate: str, executionTime: str,
                numScenesMatched: str, resultCode: str, runScriptOutput: str, runSummary: str,
                runOptions: RunOptions, datasets: str, catalogId: str, lastRunDate: str,
                orderIds: str, bulkIds: str):
        self.runId = runId
        self.subscriptionId = subscriptionId
        self.runDate = runDate
        self.executionTime = executionTime
        self.numScenesMatched = numScenesMatched
        self.resultCode = resultCode
        self.runScriptOutput = runScriptOutput
        self.runSummary = runSummary
        self.runOptions = runOptions
        self.datasets = datasets
        self.catalogId = catalogId
        self.lastRunDate = lastRunDate
        self.orderIds = orderIds
        self.bulkIds = bulkIds
        super().__init__()

    def __repr__(self):
        return {
            "runId": self.runId,
            "subscriptionId": self.subscriptionId,
            "runDate": self.runDate,
            "executionTime": self.executionTime,
            "numScenesMatched": self.numScenesMatched,
            "resultCode": self.resultCode,
            "runScriptOutput": self.runScriptOutput,
            "runSummary": self.runSummary,
            "runOptions": self.runOptions,
            "datasets": self.datasets,
            "catalogId": self.catalogId,
            "lastRunDate": self.lastRunDate,
            "orderIds": self.orderIds,
            "bulkIds": self.bulkIds
        }

    def __str__(self):
        return str(self.__repr__())

class SubscriptionDataset(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#subscriptionDataset[]
    """
    def __init__(self, datasetName: str):
        self.datasetName = datasetName
        super().__init__()

    def __repr__(self):
        return {
            "datasetName": self.datasetName
        }

    def __str__(self):
        return str(self.__repr__())

class TramOrder(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#tramOrder
    """
    def __init__(self, orderId: int, username: str, processingPriority: int, orderComment: str,
                statusCode: str, statusCodeText: str, dateEntered: str, lastUpdateDate: str):
        self.orderId = orderId
        self.username = username
        self.processingPriority = processingPriority
        self.orderComment = orderComment
        self.statusCode = statusCode
        self.statusCodeText = statusCodeText
        self.dateEntered = dateEntered
        self.lastUpdateDate = lastUpdateDate
        super().__init__()

    def __repr__(self):
        return {
            "orderId": self.orderId,
            "username": self.username,
            "processingPriority": self.processingPriority,
            "orderComment": self.orderComment,
            "statusCode": self.statusCode,
            "statusCodeText": self.statusCodeText,
            "dateEntered": self.dateEntered,
            "lastUpdateDate": self.lastUpdateDate
        }

    def __str__(self):
        return str(self.__repr__())

class TramUnit(object):
    """
    https://m2m.cr.usgs.gov/api/docs/datatypes/#tramUnit
    """
    def __init__(self, unitNumber: int, productCode: str, productName: str, datasetId: str,
                datasetName: str, collectionName: str, orderingId: str, unitPrice: str,
                unitComment: str, statusCode: str, statusCodeText: str, lastUpdatedDate: str):
        self.unitNumber = unitNumber
        self.productCode = productCode
        self.datasetId = datasetId
        self.datasetName = datasetName
        self.collectionName = collectionName
        self.orderingId = orderingId
        self.unitPrice = unitPrice
        self.unitComment = unitComment
        self.statusCode = statusCode
        self.statusCodeText = statusCodeText
        self.lastUpdatedDate = lastUpdatedDate
        super().__init__()

    def __repr__(self):
        return {
            "unitNumber": self.unitNumber,
            "productCode": self.productCode,
            "datasetId": self.datasetId,
            "datasetName": self.datasetName,
            "collectionName": self.collectionName,
            "orderingId": self.orderingId,
            "unitPrice": self.unitPrice,
            "unitComment": self.unitComment,
            "statusCode": self.statusCode,
            "statusCodeText": self.statusCodeText,
            "lastUpdatedDate": self.lastUpdatedDate
        }

    def __str__(self):
        return str(self.__repr__())
