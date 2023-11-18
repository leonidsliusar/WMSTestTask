import pytest
from crudTest.dal import add_multiple, get_all, get_many
from crudTest.models import Category, Product


@pytest.mark.django_db
@pytest.mark.parametrize('model, stub_obj_set', [(Category, 'category')],
                         indirect=['stub_obj_set'])
def test_add_multiple_get(model, stub_obj_set):
    add_multiple(model, stub_obj_set)
    assert get_all(model) == stub_obj_set


@pytest.mark.django_db
@pytest.mark.parametrize('model, stub_obj_set', [([Category, Product], ['category', 'product'])],
                         indirect=['stub_obj_set'])
def test_add_multiple_get_cascade(model, stub_obj_set):
    add_multiple(model[0], stub_obj_set[0])
    assert get_all(model[0]) == stub_obj_set[0]
    add_multiple(model[1], stub_obj_set[1])
    assert get_all(model[1]) == stub_obj_set[1]


@pytest.mark.django_db
@pytest.mark.parametrize('model, stub_obj_set', [(Category, 'category')],
                         indirect=['stub_obj_set'])
def test_get_many(model, stub_obj_set):
    add_multiple(model, stub_obj_set)
    assert get_many(model, [x.id for x in stub_obj_set]) == stub_obj_set
