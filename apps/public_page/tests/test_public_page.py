from django_tenants.urlresolvers import reverse
from django.utils import timezone
from django_tenants.test.cases import FastTenantTestCase
from django_tenants.test.client import TenantClient
from apps.public_page.views import HomeView


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
