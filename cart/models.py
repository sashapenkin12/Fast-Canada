from django.db import models
from django.contrib.auth.models import User

from household_chemicals.models import ChemicalProduct


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ChemicalProduct, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.__str__()} x {self.count}'
