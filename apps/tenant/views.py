from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


class TenantHomeView(TemplateView):
    template_name = "tenants/index.html"

    def get_context_data(self, **kwargs):
        self.request.session["tenant"] = f"{self.request.tenant}"
        kwargs["tenant_name"] = f"{self.request.tenant}"
        return kwargs


class LoginView(auth_views.LoginView):
    template_name = "tenants/login.html"
    redirect_authenticated_user = True
