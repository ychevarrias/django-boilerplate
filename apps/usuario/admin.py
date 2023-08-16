from django.contrib import admin
from tenant_users.permissions.models import UserTenantPermissions
from apps.usuario.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["password"]
    readonly_fields = ["last_login", "date_joined"]


@admin.register(UserTenantPermissions)
class UserTenantPermissionsAdmin(admin.ModelAdmin):
    filter_horizontal = ["groups", "user_permissions"]
    readonly_fields = ["profile"]
