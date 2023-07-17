from django_tenants.urlresolvers import reverse
from django.utils import timezone
from django_tenants.test.cases import FastTenantTestCase
from django_tenants.test.client import TenantClient
from apps.public_page.views import HomeView
from apps.tenant.models import Domain
from django.test import TestCase, override_settings


class TenantPublicPageTest(FastTenantTestCase):


    @classmethod
    def get_test_tenant_domain(cls):
        return 'public.fast-test.com'


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
    def get_test_tenant_domain(cls):
        return 'public.fast-test.com'


    @classmethod
    def get_test_schema_name(cls):
        return 'public'

    def get_verbosity():
        return 0

    def setUp(self):
        super().setUp()
        self.c = TenantClient(self.tenant)

    
    @override_settings(DOMAIN_SUFFIX=".fast-test.com")    
    def test_correct_creation(self):
        response = self.c.post(
            reverse("public_page:create_tenant", urlconf='webapp.urls_public'),
            data={
                "domain": "other-tenant",
                "schema_name": "other_tenant",
                "entity_name": "Other Tenant",
            }
        )
        self.assertEqual(response.status_code, 302)
        count_regs = Domain.objects.filter(
            domain__exact='other-tenant.fast-test.com',
            tenant__schema_name='other_tenant'
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
        self.assertEqual(response.status_code, 400)
