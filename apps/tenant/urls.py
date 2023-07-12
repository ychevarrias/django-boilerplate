from django.urls import path
from django.views.generic import TemplateView
from .views import TenantHomeView

app_name='tenant'


urlpatterns = [
    path("", TenantHomeView.as_view(), name="home"),
]
