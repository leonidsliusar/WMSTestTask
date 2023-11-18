import pytest


@pytest.mark.django_db
def test_get_recursive_nested(dummy_insert):
    assert dummy_insert.recursive_nested == 'Level-3 · Level-2 · Level-1'
