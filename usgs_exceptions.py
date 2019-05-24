"""
Custom exception definitions for USGS EarthExplorer API responses.
See https://earthexplorer.usgs.gov/inventory/documentation/errors for source information
TODO: Not used by the API code yet. Start with authentication.
"""

from requests.exceptions import RequestException



# ERROR TYPE DIVIDER
class USGSGeneralError(RequestException):
    """
    USGS server sent a general error response
    """

class ConversionError(USGSGeneralError):
    """
    An error occurred while attempting to convert coordinates from grid system to lat/lng
    """

class InputFormatError(USGSGeneralError):
    """
    An error occurred while decoding the service input
    """

class NotFoundError(USGSGeneralError):
    """
    A resource that has been requested could not be found
    """

class OfflineError(USGSGeneralError):
    """
    The service is currently offline
    """

class RateLimitError(USGSGeneralError):
    """
    A rate limit was encountered
    """

class UnknownError(USGSGeneralError):
    """
    An uncatchable internal server error occurred
    """

# ERROR TYPE DIVIDER

class USGSAuthenticationError(RequestException):
    """
    USGS server sent an authentication error response
    """

class AuthNoSSLError(USGSAuthenticationError):
    """
    SSL is required for the executed request
    """

class AuthInvalidError(USGSAuthenticationError):
    """
    Invalid login credentials
    """

class AuthUnauthorizedError(USGSAuthenticationError):
    """
    An invalid or expired API key was used
    """

class AuthError(USGSAuthenticationError):
    """
    An error occurred during authorization
    """

# ERROR TYPE DIVIDER

class USGSDatasetError(RequestException):
    """
    USGS server sent a dataset error response
    """

class DatasetEmptyError(USGSDatasetError):
    """
    A dataset name was not given
    """

class DatasetError(USGSDatasetError):
    """
    Could not validate dataset - Server Error
    """

class DatasetInvalidError(USGSDatasetError):
    """
    The dataset is not a valid dataset
    """

class DatasetUnavailableError(USGSDatasetError):
    """
    The dataset is valid dataset but not available to the node
    """

class DatasetNotConfiguredError(USGSDatasetError):
    """
    The dataset is available but not configured for use
    """

class DatasetOfflineError(USGSDatasetError):
    """
    The dataset exists but is offline and not available for searching
    """

class DatasetUnauthorizedError(USGSDatasetError):
    """
    The user does not have access to this dataset
    """

# ERROR TYPE DIVIDER

class USGSDownloadError(RequestException):
    """
    USGS server sent a download error response
    """

class DownloadError(USGSDownloadError):
    """
    An error occurred while looking up downloads
    """

class DowloadRateLimitError(USGSDownloadError):
    """
    The number of unattampted downloads has been exceeded
    """

# ERROR TYPE DIVIDER

class USGSItemBasketError(RequestException):
    """
    USGS server sent an item basket error response
    """

class ItemBasketError(USGSItemBasketError):
    """
    An error occurred while interacting with the item basket
    """

class ItemBasketEmptyParameterError(USGSItemBasketError):
    """
    An empty product parameter was detected
    """

class ItemBasketInvalidParameter(USGSItemBasketError):
    """
    An invalid product parameter was detected
    """

# ERROR TYPE DIVIDER

class USGSExportError(RequestException):
    """
    USGS server sent an export error response
    """

class ExportError(USGSExportError):
    """
    An error occurred while creating or processing an export request
    """

class ExportUnauthorizedError(USGSExportError):
    """
    This user cannot access the given export
    """

class ExportPendingError(USGSExportError):
    """
    The requested export has not been generated
    """

class ExportNotFoundError(USGSExportError):
    """
    Invalid Export ID
    """

# ERROR TYPE DIVIDER

class USGSMetadataError(RequestException):
    """
    USGS server sent a metadata error response
    """

class MetadataError(USGSMetadataError):
    """
    An error occurred while searching for metadata
    """

class MetadataScenesInvalidError(USGSMetadataError):
    """
    One or more scenes are invalid
    """

class MetadataScenesEmptyError(USGSMetadataError):
    """
    No scenes were given for metadata search
    """

# ERROR TYPE DIVIDER

class USGSNodeCatalogError(RequestException):
    """
    USGS server sent a node or catalog error response
    """

class NodeEmptyError(USGSNodeCatalogError):
    """
    A node parameter was not passed
    """

class NodeUnauthorizedError(USGSNodeCatalogError):
    """
    An unauthorized node was used
    """

class NodeUnsupportedMethodError(USGSNodeCatalogError):
    """
    The called method is not supported for the node provided
    """

class CatalogUnknownError(USGSNodeCatalogError):
    """
    An unknown catalogId was used
    """

# ERROR TYPE DIVIDER

class USGSNotificationError(RequestException):
    """
    An error occurred while returning system notifications
    """

# ERROR TYPE DIVIDER

class USGSOrderError(RequestException):
    """
    USGS server sent an order error response
    """

class InvalidOrderError(USGSOrderError):
    """
    The order is invalid or unauthorized
    """

class OrderError(USGSOrderError):
    """
    An error occurred while retrieving order information
    """

# ERROR TYPE DIVIDER

class USGSProductsEmptyError(RequestException):
    """
    No products were given for download or order
    """

# ERROR TYPE DIVIDER

class USGSSearchError(RequestException):
    """
    USGS server sent a search error response
    """

class SearchError(USGSSearchError):
    """
    An error occurred while searching for data
    """

class SearchInvalidParamError(USGSSearchError):
    """
    An invalid search parameter was given
    """

# ERROR TYPE DIVIDER

class USGSSubscriptionRunninError(RequestException):
    """
    The requested subscription is already running
    """