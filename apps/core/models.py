from ckeditor.fields import RichTextField
from django.db import models
from filebrowser.fields import FileBrowseField


class InfoSite(models.Model):
    terminos_y_condiciones = RichTextField(blank=True, default="")
    favicon = FileBrowseField(
        "Favicon", max_length=200,
        directory="favicon/", extensions=[".jpg", ".png"], blank=True
    )