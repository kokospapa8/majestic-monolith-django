from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import exceptions
from rest_framework.exceptions import Throttled
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.settings import api_settings
from rest_framework.views import exception_handler


class ErrorsFormatter:
    """
    The current formatter gets invalid serializer errors,
    uses DRF standart for code and messaging
    and then parses it to the following format:
    {
        "errors": [
            {
                "message": "Error message",
                "code": "Some code",
                "field": "field_name"
            },
            {
                "message": "Error message",
                "code": "Some code",
                "field": "nested.field_name"
            },
            ...
        ]
    }
    """

    FIELD = "field"
    MESSAGE = "message"
    CODE = "code"
    ERRORS = "errors"

    def __init__(self, exception):
        self.exception = exception

    def __call__(self):
        if hasattr(self.exception, "get_full_details"):
            formatted_errors = self._get_response_json_from_drf_errors(
                serializer_errors=self.exception.get_full_details()
            )
        else:
            formatted_errors = self._get_response_json_from_error_message(
                message=str(self.exception)
            )

        return formatted_errors

    def _get_response_json_from_drf_errors(self, serializer_errors=None):
        if serializer_errors is None:
            serializer_errors = {}

        if type(serializer_errors) is list:
            serializer_errors = {api_settings.NON_FIELD_ERRORS_KEY: serializer_errors}

        list_of_errors = self._get_list_of_errors(errors_dict=serializer_errors)

        response_data = {self.ERRORS: list_of_errors}

        return response_data

    def _get_response_json_from_error_message(
        self, *, message="", field=None, code="error"
    ):
        response_data = {self.ERRORS: [{self.MESSAGE: message, self.CODE: code}]}

        if field:
            response_data[self.ERRORS][self.FIELD] = field

        return response_data

    def _unpack(self, obj):
        if type(obj) is list and len(obj) == 1:
            return obj[0]

        return obj

    def _get_list_of_errors(self, field_path="", errors_dict=None):
        """
        Error_dict is in the following format:
        {
            'field1': {
                'message': 'some message..'
                'code' 'some code...'
            },
            'field2: ...'
        }
        """
        if errors_dict is None:
            return []

        message_value = errors_dict.get(self.MESSAGE, None)

        # Note: If 'message' is name of a field we don't want to stop the recursion here!
        if message_value is not None and (
            type(message_value) in {str, exceptions.ErrorDetail}
        ):
            if field_path:
                errors_dict[self.FIELD] = field_path
            return [errors_dict]

        errors_list = []
        for key, value in errors_dict.items():
            new_field_path = "{0}.{1}".format(field_path, key) if field_path else key
            key_is_non_field_errors = key == api_settings.NON_FIELD_ERRORS_KEY

            if type(value) is list:
                current_level_error_list = []
                new_value = value

                for error in new_value:
                    # if the type of field_error is list we need to unpack it
                    field_error = self._unpack(error)

                    if not key_is_non_field_errors:
                        field_error[self.FIELD] = new_field_path

                    current_level_error_list.append(field_error)
            else:
                path = field_path if key_is_non_field_errors else new_field_path

                current_level_error_list = self._get_list_of_errors(
                    field_path=path, errors_dict=value
                )

            errors_list += current_level_error_list

        return errors_list


def custom_exception_handler(exc, context):
    def _parse_throttle_classes(throttle_classes: list) -> str:
        ret = []
        for throttle in throttle_classes:
            name = throttle.__name__
            rate = throttle().get_rate()
            ret.append(f"{name}({rate})")
        return ", ".join(ret)

    # Call REST framework's default exception handler first, to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        return response

    formatter = ErrorsFormatter(exc)
    response.data = formatter()

    if isinstance(exc, DjangoValidationError) or isinstance(exc, DRFValidationError):
        if hasattr(exc, "detail"):

            if isinstance(exc.detail, dict):
                non_field_errors = exc.detail.get(
                    "non_field_errors", None
                )  # serializer.validate() errors
                if non_field_errors:
                    response.data = {"detail": ", ".join(non_field_errors)}

            if isinstance(exc.detail, list):
                response.data = {
                    "detail": ", ".join(exc.detail),
                    "error": ", ".join(exc.detail),  # TEMP
                }

    # check throttle exceptions
    if isinstance(exc, Throttled):
        throttle_class_name = _parse_throttle_classes(context["view"].throttle_classes)
        throttle_errors = f"Throttled by {throttle_class_name}. {exc.wait} seconds left to be released."

        # create custom response data
        throttled_response = {"detail": throttle_errors}
        response.data = throttled_response
    return response
