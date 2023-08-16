from django.conf import settings
from django_tenants.test.cases import FastTenantTestCase as FastTenantTestCaseLegacy
from django_tenants.utils import get_tenant_model, get_tenant_domain_model, get_public_schema_name
from django.db import connection
from apps.core.multi_tenant_utils.tasks import provision_tenant
from apps.core.multi_tenant_utils.utils import create_public_tenant

from apps.usuario.models import User


class FastTenantTestCase(FastTenantTestCaseLegacy):

    @classmethod
    def get_test_schema_name(cls):
        return 'fast-test'

    @classmethod
    def get_test_tenant_domain(cls):
        if cls.get_test_schema_name() == get_public_schema_name():
            return settings.TENANT_USERS_DOMAIN
        return f'{cls.get_test_schema_name()}.{settings.TENANT_USERS_DOMAIN}'

    @classmethod
    def setup_test_tenant_and_domain(cls):
        user_email = f"admin@{cls.get_test_tenant_domain()}"
        public_schema_name = get_public_schema_name()
        already_public = get_tenant_model().objects.filter(
            schema_name=public_schema_name
        ).exists()
        owner = None
        if not already_public:
            create_public_tenant(
                domain_url=settings.TENANT_USERS_DOMAIN,
                owner_email=user_email,
                owner_as_root=True,
                owner_password="s0m3_sup3r_passw0rd"
            )
        elif not User.objects.filter(email=user_email).exists():
            owner = User.objects.create_user(
                email=user_email,
                password='password',
                is_active=True
            )
        if owner is None:
            owner = User.objects.filter(email=user_email).first()

        cls.tenant = get_tenant_model().objects.filter(
            schema_name__startswith=f"{cls.get_test_schema_name()}"
        ).first()
        if cls.tenant is None:
            provision_tenant(
                tenant_name="TestTenant",
                tenant_slug=cls.get_test_schema_name(),
                user_email=user_email,
                verbosity=1,
                add_timestamp=False,
            )
            cls.tenant = get_tenant_model().objects.filter(
                schema_name__startswith=f"{cls.get_test_schema_name()}"
            ).first()
        try:
            cls.tenant.add_user(owner)
        except:
            pass
        cls.use_new_tenant()

        # cls.tenant = get_tenant_model()(schema_name=cls.get_test_schema_name())
        # cls.setup_tenant(cls.tenant)
        # cls.tenant.save(verbosity=cls.get_verbosity())
        #
        # # Set up domain
        # tenant_domain = cls.get_test_tenant_domain()
        # cls.domain = get_tenant_domain_model()(tenant=cls.tenant, domain=tenant_domain)
        # cls.setup_domain(cls.domain)
        # cls.domain.save()
        # cls.use_new_tenant()

    @classmethod
    def setUpClass(cls):
        cls.add_allowed_test_domain()
        tenant_model = get_tenant_model()

        test_schema_name = cls.get_test_schema_name()
        tenant_query = tenant_model.objects.filter(
            schema_name__startswith=f"{test_schema_name}"
        )
        if tenant_query.exists():
            cls.tenant = tenant_query.first()
            cls.use_existing_tenant()
        else:
            cls.setup_test_tenant_and_domain()

        connection.set_tenant(cls.tenant)
