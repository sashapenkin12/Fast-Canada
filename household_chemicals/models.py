from django.db import models


class ChemicalProduct(models.Model):
    title: models.CharField = models.CharField(max_length=100)
    full_description: models.CharField = models.TextField()
    price: models.IntegerField = models.IntegerField()
    is_available: models.BooleanField = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.title
