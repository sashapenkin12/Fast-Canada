"""
Exception handlers for API.
"""

from typing import Dict, Any, Optional

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

def custom_exception_handler(
        exc: Exception,
        context: Dict[str, Any],
) -> Response:
    """
    Handles all uncaught exceptions in API.

    Args:
        exc: Occurred exception.
        context: Exception context.

    Returns:
        Response: Response with exception details, or just with 500 status code.
    """
    response: Optional[Response] = exception_handler(exc, context)

    if response is not None:

        response.data = {
            'error': True,
            'status_code': response.status_code,
            'message': response.data.get('detail', 'An error has occurred'),
            'details': response.data if 'detail' not in response.data else {},
        }
    else:
        return Response({
            'error': True,
            'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Internal server error.'
        }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    return response