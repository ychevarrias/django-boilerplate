from django.utils import timezone
from rest_framework.exceptions import APIException, status
from django.utils.translation import gettext_lazy as _


class ServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = 'server_error'
    default_detail = {
        "type": "backend",
        "message": _('El sistema tuvo un error al procesar su solicitud.'),
        "code": "server_error",
        "server-start-time": timezone.now()
    }


class ItemAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = 'server_error'
    default_detail = {
        "type": "backend",
        "message": _('Ya existe un registro igual en el sistema'),
        "code": "server_error",
        "server-start-time": timezone.now()
    }