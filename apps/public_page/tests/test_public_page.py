from django.conf import settings
from django_tenants.urlresolvers import reverse
from django.utils import timezone
from django_tenants.test.cases import FastTenantTestCase
from django_tenants.test.client import TenantClient
from apps.public_page.views import HomeView
from apps.tenant.models import Domain
from django.test import TestCase, override_settings
from apps.core.utils.public_tokens import PUBLIC_TOKEN_KEY
from django.core.cache import cache
from apps.core.test_utils import FastTenantTestCase


class TenantPublicPageTest(FastTenantTestCase):

    @classmethod
    def get_test_schema_name(cls):
        return 'public'

    def setUp(self):
        super().setUp()
        self.c = TenantClient(self.tenant)

    def test_user_profile_view(self):
        response = self.c.get(reverse("public_page:home", urlconf='webapp.urls_public'))
        self.assertIn(b'PublicHomePage', response.content, "No respondió la vista pública")
        self.assertEqual(response.status_code, 200)


class TenantCreationTest(FastTenantTestCase):

    @classmethod
    def get_test_schema_name(cls):
        return 'public'

    @classmethod
    def get_verbosity(cls):
        return 0

    def setUp(self):
        super().setUp()
        self.c = TenantClient(
            self.tenant,
            HTTP_USER_AGENT='Mozilla/5.0',
        )

    def test_correct_creation(self):
        response = self.c.get(
            reverse("public_page:pin_request", urlconf='webapp.urls_public'),
            headers={
                "referer": "https://fast-test.com/example/"
            }
        )
        self.assertIn(response.status_code, [200, 201])
        response = self.c.post(
            reverse("public_page:create_tenant", urlconf='webapp.urls_public'),
            data={
                "domain": "other-tenant",
                "schema_name": "other_tenant",
                "entity_name": "Other Tenant",
                "token": cache.get(PUBLIC_TOKEN_KEY, ''),
            },
        )
        self.assertEqual(response.status_code, 302)
        count_regs = Domain.objects.filter(
            domain__exact=f'other-tenant.{settings.TENANT_USERS_DOMAIN}',
        ).count()
        self.assertEqual(count_regs, 1, "No se registró el nuevo Tenant")

    def test_fail_creation(self):
        response = self.c.post(
            reverse("public_page:create_tenant", urlconf='webapp.urls_public'),
            data={
                "domain": "other-tenant.fast-test.com",
                "schema_name": "other_tenant",
                "entity_name": "Other Tenant",
            }
        )
        print("response.request -->>", response.request)
        self.assertEqual(response.status_code, 400)
