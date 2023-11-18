from typing import TypeVar, Type

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    parent = models.OneToOneField('self', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    @property
    def get_nested(self) -> str:
        current_parent = self.parent
        nested = f'{self.title}'
        while current_parent:
            nested += f' · {current_parent.title}'
            current_parent = current_parent.parent
        return nested


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    category_id = models.OneToOneField(Category, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)])
    cost = models.DecimalField(null=False, max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.title} {self.cost} {self.count} {self.category_id}'


M = TypeVar('M', Type[Category], Type[Product])
