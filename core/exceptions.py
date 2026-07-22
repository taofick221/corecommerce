from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is None:
        return response

    message = "Request failed"

    if isinstance(response.data, dict):
        message = response.data.get(
            "detail",
            "Validation error",
        )

    response.data = {
        "success": False,
        "status_code": response.status_code,
        "message": message,
        "errors": response.data,
    }

    return response
