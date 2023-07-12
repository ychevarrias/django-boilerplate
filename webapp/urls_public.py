"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from filebrowser.sites import site
from apps.core.utils.development import TemplateRender
from apps.public_page.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]

if settings.URL_PREFIX:
    urlpatterns = [path('%s/' % settings.URL_PREFIX, include(urlpatterns))]

if settings.DEBUG:
    dev_patterns = []
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        re_path(r'(?P<path>.*)\.html$', TemplateRender.as_view()),
    ]
    if settings.FRONTEND_MODE:
        urlpatterns += [path(r'', TemplateRender.as_view())]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

