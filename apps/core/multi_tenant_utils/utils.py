from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import connection
from django_tenants.utils import (
    get_public_schema_name,
    get_tenant_domain_model,
    get_tenant_model,
)
from tenant_users.tenants.models import ExistsError


def get_current_tenant():
    current_schema = connection.schema_name
    TenantModel = get_tenant_model()
    tenant = TenantModel.objects.get(schema_name=current_schema)
    return tenant


def create_public_tenant(domain_url, owner_email, **owner_extra):
    """
    domain_url: 'example.com'
    owner_email: 'admin@example.com'
    **owner_extra: props for user_instance

    Returns: User instance

    """
    UserModel = get_user_model()
    TenantModel = get_tenant_model()
    public_schema_name = get_public_schema_name()

    owner_as_root = owner_extra.pop("owner_as_root", False)
    owner_password = owner_extra.pop("owner_password", None)

    if TenantModel.objects.filter(schema_name=public_schema_name).exists():
        raise ExistsError('Public tenant already exists')

    # Create public tenant user. This user doesn't go through object manager
    # create_user function because public tenant does not exist yet
    profile = UserModel.objects.create(
        email=owner_email,
        is_active=True,
        **owner_extra,
    )
    profile.set_unusable_password()
    profile.save()


    # Create public tenant
    public_tenant = TenantModel.objects.create(
        schema_name=public_schema_name,
        name='Public Tenant',
        owner=profile,
    )

    # Add one or more domains for the tenant
    get_tenant_domain_model().objects.create(
        domain=domain_url,
        tenant=public_tenant,
        is_primary=True,
    )

    # Add system user to public tenant (no permissions)
    public_tenant.add_user(profile)

    # Update system user for public tenant (permissions/password)
    user_perms = profile.tenant_perms
    user_perms.is_staff = True

    if owner_password:
        profile.set_password(owner_password)

    if owner_as_root:
        user_perms.is_superuser = True

    user_perms.save()
    profile.save(update_fields=["password"])
    return profile
