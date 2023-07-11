from django.conf import settings

from apps.core.models import InfoSite


def global_context(request):
    return {
        "infosite": InfoSite.objects.last()
    }
