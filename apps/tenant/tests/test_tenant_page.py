from django_tenants.urlresolvers import reverse
from django.utils import timezone
from django_tenants.test.cases import FastTenantTestCase
from django_tenants.test.client import TenantClient
from django.test import tag
from apps.core.test_utils import FastTenantTestCase


class TenantHomePageTest(FastTenantTestCase):

    def setUp(self):
        super().setUp()
        self.c = TenantClient(self.tenant)

    def test_home_view(self):
        response = self.c.get(reverse('tenant:home'))
        self.assertEqual(response.status_code, 200)


class TenantLoginPageTest(FastTenantTestCase):

    def setUp(self):
        super().setUp()
        self.c = TenantClient(self.tenant)

    @tag("views")
    def test_login_view(self):
        response = self.c.get(reverse('tenant:login'))
        # print(self.tenant, dir(response))
        # print(response.request)
        self.assertEqual(response.status_code, 200)

