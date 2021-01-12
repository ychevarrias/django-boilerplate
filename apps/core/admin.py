from django.contrib import admin
from .models import InfoSite


@admin.register(InfoSite)
class InfoSiteAdmin(admin.ModelAdmin):
    model = InfoSite
