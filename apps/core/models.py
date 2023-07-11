from ckeditor.fields import RichTextField
from django.db import models


class InfoSite(models.Model):
    terminos_y_condiciones = RichTextField(blank=True, default="")
    favicon = models.ImageField(
        "Favicon", upload_to="favicon/", blank=True
    )
