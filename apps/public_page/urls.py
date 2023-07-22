from django.urls import path
from django.views.generic import TemplateView
from .views import HomeView, CreateTenantView, PINRequestView
app_name = 'public_page'


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("ec0a499c-618d-4bf0-aeaa-a65b9f026b5d/", CreateTenantView.as_view(), name="create_tenant"),
    path("57b4a601-b38a-4fef-a553-e35df47a15ce/", PINRequestView.as_view(), name="pin_request"),
]
