from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from apps.tenant.models import Client, Domain


class DomainRegister(forms.Form):
    domain = forms.CharField(max_length=32)
    schema_name = forms.CharField(max_length=32)
    entity_name = forms.CharField(max_length=64)

    @staticmethod
    def check_FQDN(value):
        if "." in value:
            raise ValidationError("No puede contener puntos")
        try:
            value.encode('ascii')
        except UnicodeEncodeError:
            raise ValidationError("contiene caracteres especiales no admitidos")
        allowed = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
        if not allowed.match(value):
            raise ValidationError("con cumple con las reglas FQDN")
        return value

    def clean_schema_name(self):
        value = self.cleaned_data['schema_name'].lower()
        if '-' in value:
            raise ValidationError("El schema no puede contener giones medios")
        self.check_FQDN(value.replace("_", '-'))
        if Client.objects.filter(schema_name__iexact=value).exists():
            raise ValidationError("El schema está en uso")
        return value

    def clean_domain(self):
        value = self.cleaned_data['domain']
        if "_" in value:
            raise ValidationError("No puede contener guiones bajos")
        self.check_FQDN(value)
        if Client.objects.filter(domains__domain__iexact=value).exists():
            raise ValidationError("El dominio está en uso")
        return value

    def create_domain(self):
        from django_tenants.utils import schema_context
        with schema_context("public"):
            client = Client(
                schema_name=self.cleaned_data["schema_name"],
                name=self.cleaned_data["entity_name"],
                on_trial=False,
                paid_until=timezone.localtime(),
            )
            client.save(verbosity=0)
            client.domains.create(
                domain=self.get_domain(), is_primary=True
            )

    def get_domain(self):
        return f"{self.cleaned_data['domain']}{settings.DOMAIN_SUFFIX}"

    def get_success_url(self):
        protocol = 'https'
        if "local" in settings.DOMAIN_SUFFIX:
            protocol = 'http'
        return f"{protocol}://{self.get_domain()}"