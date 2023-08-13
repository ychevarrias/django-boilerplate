import logging
from django.conf import settings
from django.db import models
from django.utils import timezone
from django_tenants.models import TenantMixin, DomainMixin
from django.utils.text import slugify
logger = logging.getLogger(__name__)


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(auto_now_add=True)
    on_trial = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True

    @staticmethod
    def get_valid_schema_name(name):
        assert isinstance(name, str), "El nombre debe ser un String"
        name = slugify(name).replace("-", "_")
        if name and name[0].isnumeric():
            name = f"a_{name}"
        return name

    @classmethod
    def create_client(cls, name):
        assert isinstance(name, str), "El nombre debe ser un String"
        name = name.strip()
        client = cls(
            name=name,
            paid_until=timezone.localtime(),
            on_trial=False,
            created_on=timezone.localtime(),
            schema_name=cls.get_valid_schema_name(name)
        )
        client.save()
        if client.schema_name == 'public':
            client.domains.create(
                domain=f"{settings.DOMAIN_SUFFIX[1:]}",
            )
            return client
        domain_name = client.schema_name.replace("_", "-")
        domain = client.domains.create(
            domain=f"{domain_name}{settings.DOMAIN_SUFFIX}",
        )
        protocol = 'https'
        if settings.DOMAIN_SUFFIX.endswith(".localhost"):
            protocol = 'http'
        logger.info(f"{protocol}://{domain.domain}")
        return client


class Domain(DomainMixin):
    pass
