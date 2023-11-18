import pytest

from crudTest.utils import StringParserFactory, StringParser, get_obj_set
from crudTest.data_models import CategoryBase, ProductBase
from crudTest.models import Category


@pytest.mark.parametrize('parser, stub_map', [('product', 'product'), ('category', 'category')], indirect=True)
def test_map_from_str(parser, stub_map):
    assert parser.map_from_str == stub_map


@pytest.mark.parametrize('stub_string, model, stub_map_key', [('category', CategoryBase, 'category'),
                                                              ('product', ProductBase, 'products')],
                         indirect=['stub_string', 'stub_map_key'])
def test_prepare(stub_string, model, stub_map_key):
    parser = StringParserFactory(stub_string).prepare
    assert isinstance(parser, StringParser)
    assert parser.base_model is model
    assert parser.map_key == stub_map_key


@pytest.mark.parametrize('stub_map, stub_obj_set', [('category', 'category')], indirect=True)
def test_get_obj_set(stub_map, stub_obj_set):
    assert get_obj_set(stub_map, Category) == stub_obj_set
