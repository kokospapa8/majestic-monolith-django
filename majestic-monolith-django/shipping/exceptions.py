from rest_framework import status
from core.exceptions import CustomTextAPIException


class ShippingTransportCompletedException(CustomTextAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "ShippingTransport already completed."
    default_code = 'ShippingTransportAlreadyCompleted'


class ShippingTransportDistributionNotConfiguredException(CustomTextAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "ShippingTransport distribution center not assigned."
    default_code = 'ShippingTransportDistributionNotConfigured'


class ShippingTransportDriverNotConfiguredException(CustomTextAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "driver is not assigned."
    default_code = 'ShippingTransportDriverNotConfigured'


class ShippingTransportBatchNotExistException(CustomTextAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "ShippingBatch does not exists."
    default_code = 'ShippingBatchNotExist'


class ShippingTransportBatchAlreadyCompletedException(CustomTextAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "ShippingBatch already completed."
    default_code = 'ShippingBatchAlreadyCompleted'


class ShippingBatchCompletedException(CustomTextAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "ShippingBatch already completed."
    default_code = 'ShippingBatchCompleted'


class ShippingBatchItemAlreadyExsitException(CustomTextAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "ShippingItem does not exists."
    default_code = 'ShippingBatchItemAlreadyExsit'


class ShippingBatchItemAddInvalidStatusException(CustomTextAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "ShippingItem in invalid status."
    default_code = 'ShippingBatchItemAddInvalidStatus'


class ShippingTransportNoBatchException(CustomTextAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No Batch assigned to transport."
    default_code = 'ShippingTransportNoBatch'
