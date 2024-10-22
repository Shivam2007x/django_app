from rest_framework.views import exception_handler #type: ignore

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response



# Allows customization of error responses in APIs.
# Can add additional data or modify the response format.
