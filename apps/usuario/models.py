from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from tenant_users.tenants.models import UserProfile
from django.utils.translation import gettext_lazy as _


class User(UserProfile):
    date_joined = models.DateTimeField(
        _("date joined"), default=timezone.now
    )


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.FileField(upload_to='photos/')
