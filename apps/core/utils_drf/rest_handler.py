from django.db import IntegrityError
from django.http import HttpResponse
from rest_framework.views import exception_handler as drf_handler
from apps.core.utils_drf.exceptions import ItemAlreadyExists


def exception_handler(exc, context):
    if isinstance(exc, IntegrityError):
        if exc.args:
            dbmsg_error = exc.args[0]
            if 'unique_reservation_valid' in dbmsg_error:
                return drf_handler(ItemAlreadyExists(), context)
        return HttpResponse('DataBase error', status=500)

    response = drf_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
    return response
