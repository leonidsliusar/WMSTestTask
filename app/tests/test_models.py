def test_get_nested(dummy_obj):
    assert dummy_obj.get_nested == 'Level-3 · Level-2 · Level-1'
