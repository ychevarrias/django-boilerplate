from django.shortcuts import render
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.views.generic import View, FormView, TemplateView
from apps.core.utils.public_tokens import check_sended, get_token
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


class PINRequestView(View):

    def get_admin_email_to(self):
        result = []
        for admin in settings.ADMINS:
            result.append(
                f"{admin[0]} <{admin[1]}>"
            )
        return result

    def get(self, request):
        print(request.headers)
        if request.META.get("HTTP_REFERER"):
            if check_sended():
                return JsonResponse({
                    "status": "already_sent"
                }, status=200)
            token = get_token()
            html_content = f"""
            <p>Su token de acceso temporal es:<br>
            <strong>{token}</strong><br>
            <small>recuerde que el tiempo es expiración es de 10 minutos</small>
            </p>
            """
            msg = EmailMessage(
                "Token de acceso",
                html_content, 
                settings.DEFAULT_FROM_EMAIL, 
                self.get_admin_email_to()
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            return JsonResponse({
                "status": "sent"
            }, status=201)
        raise Http404