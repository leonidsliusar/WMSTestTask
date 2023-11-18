import os

import pytest

from crudTest.models import Category, Product
from crudTest.utils import StringParser, ProductBase, CategoryBase

category_string = """id:title:parent
    1:Товары для дома:None
    2:Посуда для кухни:1
    3:Кастрюли:2"""

products_string = """id:title:category_id:count:cost
1:Велосипед:1:100:100.50
2:Кастрюля 1,5л:2:50:1200
3:Тарелка 25см:3:1000:25
4:Кастрюля 3л:2:55:300.78"""


@pytest.fixture
def dummy_obj_set(request) -> list:
    obj_set = []
    match request.param:
        case 'category':
            for item in stub_map_category():
                obj_set.append(Category(**item))
        case 'product':
            for item in stub_map_products():
                obj_set.append(Product(**item))
    return obj_set


@pytest.fixture
def dummy_obj() -> Category:
    obj_l_1 = Category(id=1, title='Level-1', parent=None)
    obj_l_2 = Category(id=2, title='Level-2', parent=obj_l_1)
    obj = Category(id=3, title='Level-3', parent=obj_l_2)
    return obj


@pytest.fixture()
def dummy_insert() -> Category:
    obj_l_1 = Category(id=1, title='Level-1', parent=None)
    obj_l_2 = Category(id=2, title='Level-2', parent=obj_l_1)
    obj = Category(id=3, title='Level-3', parent=obj_l_2)
    Category.objects.bulk_create([obj_l_1, obj_l_2, obj])
    return obj



@pytest.fixture
def stub_obj_set(request):
    if isinstance(request.param, list):
        return stub_obj_category(), stub_obj_product()
    else:
        match request.param:
            case 'category':
                return stub_obj_category()
            case 'product':
                return stub_obj_product()


def stub_obj_category():
    stub_map = stub_map_category()
    obj_1 = Category(**stub_map[0])
    stub_map[1]['parent'] = obj_1
    obj_2 = Category(**stub_map[1])
    stub_map[2]['parent'] = obj_2
    obj_3 = Category(**stub_map[2])
    obj_set = [obj_1, obj_2, obj_3]
    return obj_set


def stub_obj_product():
    categories_set = stub_obj_category()
    stub_map = stub_map_products()
    obj_set = []
    for item in stub_map:
        obj = [x for x in categories_set if x.id == item['category_id']][0]
        item['category_id'] = obj
        obj_set.append(Product(**item))
    return obj_set


@pytest.fixture
def stub_string(request) -> str:
    match request.param:
        case 'product':
            return products_string
        case 'category':
            return category_string


@pytest.fixture
def stub_category() -> str:
    return category_string


@pytest.fixture
def prod_category() -> str:
    return products_string


@pytest.fixture
def parser(request):
    model = None
    match request.param:
        case 'category':
            model = CategoryBase
            data_set = category_string.split('\n')
        case 'product':
            model = ProductBase
            data_set = products_string.split('\n')
    map_key = [x.strip(' ') for x in data_set[0].split(':')]
    return StringParser(data_set, map_key, model)


@pytest.fixture
def stub_map(request) -> list[dict]:
    match request.param:
        case 'product':
            return stub_map_products()
        case 'category':
            return stub_map_category()


@pytest.fixture
def stub_map_key(request) -> list:
    match request.param:
        case 'products':
            return list(stub_map_products()[0].keys())
        case 'category':
            return list(stub_map_category()[0].keys())


def stub_map_category() -> list[dict]:
    return [
        {
            'id': 1,
            'title': 'Товары для дома',
            'parent': None
        },
        {
            'id': 2,
            'title': 'Посуда для кухни',
            'parent': 1
        },
        {
            'id': 3,
            'title': 'Кастрюли',
            'parent': 2
        }
    ]


def stub_map_products() -> list[dict]:
    return [
        {
            'id': 1,
            'title': 'Велосипед',
            'category_id': 1,
            'count': 100,
            'cost': 100.50
        },
        {
            'id': 2,
            'title': 'Кастрюля 1,5л',
            'category_id': 2,
            'count': 50,
            'cost': 1200
        },
        {
            'id': 3,
            'title': 'Тарелка 25см',
            'category_id': 3,
            'count': 1000,
            'cost': 25
        },
        {
            'id': 4,
            'title': 'Кастрюля 3л',
            'category_id': 2,
            'count': 55,
            'cost': 300.78
        }
    ]
