from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import View, FormView, TemplateView
from .forms import DomainRegister


class HomeView(TemplateView):
    template_name = "public/index.html"


class CreateTenantView(FormView):
    form_class = DomainRegister
    template_name = "public/create_tenant.html"


    def form_valid(self, form):
        form.create_domain()
        return HttpResponseRedirect(form.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form), status=400
        )

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs["domain_suffix"] = settings.DOMAIN_SUFFIX
        return kwargs
