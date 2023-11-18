from typing import Optional, TypeVar, Type

from pydantic import BaseModel, field_validator

from crudTest.models import Category, Product


class ProductBase(BaseModel):
    id: int
    title: str
    category_id: int
    count: int
    cost: float

    @field_validator('id', 'count', 'category_id', mode='before')
    @classmethod
    def type_casting(cls, v: str) -> int:
        v = v.replace(' ', '')
        if v.isnumeric():
            return int(v)

    @classmethod
    @field_validator('cost', mode='before')
    def float_casting(cls, v: str) -> float:
        v = v.replace(' ', '')
        if v.isnumeric():
            return float(v)


class CategoryBase(BaseModel):
    id: int
    title: str
    parent: Optional[int] = None

    @field_validator('id', 'parent', mode='before')
    @classmethod
    def type_casting(cls, v: str) -> Optional[int]:
        v = v.replace(' ', '')
        if v == 'None':
            return
        elif v.isnumeric():
            return int(v)


T = TypeVar('T', Type[CategoryBase], Type[ProductBase])

models_mapping = {
    CategoryBase: Category,
    ProductBase: Product
}