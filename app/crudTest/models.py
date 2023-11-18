from typing import TypeVar, Type

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, connection


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    @property
    def nested(self) -> str:
        current_parent = self.parent
        nested = f'{self.title}'
        while current_parent:
            nested += f' · {current_parent.title}'
            current_parent = current_parent.parent
        return nested

    @property
    def recursive_nested(self) -> str:
        query = """
                WITH RECURSIVE category_tree(id, title, parent_id) AS (
                    SELECT id, title, parent_id
                    FROM "crudTest_category"
                    WHERE id = %s
                    UNION
                    SELECT c.id, c.title, c.parent_id
                    FROM "crudTest_category" c
                    INNER JOIN category_tree ct ON c.id = ct.parent_id
                )
                SELECT title FROM category_tree;
            """
        with connection.cursor() as cursor:
            cursor.execute(query, [self.id])
            nested = ' · '.join(row[0] for row in cursor.fetchall())
        return nested


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category_id')
    count = models.PositiveIntegerField(validators=[MaxValueValidator(100000), MinValueValidator(0)])
    cost = models.DecimalField(null=False, max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.title} {self.cost} {self.count} {self.category_id}'


M = TypeVar('M', Type[Category], Type[Product])
