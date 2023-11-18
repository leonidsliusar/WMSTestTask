import pytest


def test_get_nested(dummy_obj):
    assert dummy_obj.nested == 'Level-3 · Level-2 · Level-1'


@pytest.mark.django_db
def test_get_recursive_nested(dummy_insert):
    assert dummy_insert.recursive_nested == 'Level-3 · Level-2 · Level-1'
