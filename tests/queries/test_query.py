from sqlpuzzle._queries import Query


def test_eq():
    assert Query() != 'string'


def test_non_exist_property():
    assert not Query().has('xxx')
