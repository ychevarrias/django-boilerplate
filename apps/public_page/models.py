from django.db import models


class Packs(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField("Precio", max_digits=5, decimal_places=2)
