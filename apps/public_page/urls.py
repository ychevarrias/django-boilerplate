from django.urls import path
from django.views.generic import TemplateView
from .views import HomeView
app_name = 'public_page'


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
