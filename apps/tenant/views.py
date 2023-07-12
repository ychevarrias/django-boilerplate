from django.shortcuts import render
from django.views.generic import TemplateView


class TenantHomeView(TemplateView):
    template_name = "tenants/index.html"