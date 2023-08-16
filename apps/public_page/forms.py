import re
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.core.multi_tenant_utils.tasks import provision_tenant
from apps.core.utils.public_tokens import validate_token
from apps.tenant.models import Client, Domain
from apps.usuario.models import User


class DomainRegister(forms.Form):
    domain = forms.CharField(max_length=32)
    schema_name = forms.CharField(max_length=32)
    entity_name = forms.CharField(max_length=64)
    keep_alive_token = forms.BooleanField(required=False, initial=True)
    token = forms.CharField(max_length=16)

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

    def clean_token(self):
        value = self.cleaned_data['token']
        if not validate_token(value):
            raise ValidationError("El token no es válido o expiró")
        return value


    def clean(self):
        cleaned_data = super().clean()
        token = cleaned_data.get("token")
        keep_alive_token = cleaned_data.get("keep_alive_token", False)
        validate_token(token, not keep_alive_token)


    def create_domain(self):
        from django_tenants.utils import schema_context
        with schema_context("public"):
            user = User.objects.order_by("id").first()
            if user is None:
                user = User.objects.create_user(
                    email="root@localhost",
                    password='password',
                    is_active=True
                )
            user_email = user.email
            provision_tenant(
                tenant_name=self.cleaned_data["entity_name"],
                tenant_slug=self.cleaned_data["domain"],
                user_email=user_email,
                verbosity=0,
                add_timestamp=False,
            )

            # client = Client(
            #     schema_name=self.cleaned_data["schema_name"],
            #     name=self.cleaned_data["entity_name"],
            #     on_trial=False,
            #     paid_until=timezone.localtime(),
            # )
            # client.save(verbosity=0)
            # client.domains.create(
            #     domain=self.get_domain(), is_primary=True
            # )

    def get_domain(self):
        return f"{self.cleaned_data['domain']}{settings.DOMAIN_SUFFIX}"

    def get_success_url(self):
        protocol = 'https'
        if "local" in settings.DOMAIN_SUFFIX:
            protocol = 'http'
        return f"{protocol}://{self.get_domain()}"

    class Meta:
        widgets = {
            'domain': forms.TextInput(attrs={'autocomplete': 'off'}),
            'schema_name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'entity_name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'token': forms.TextInput(attrs={'autocomplete': 'off'}),
        }
