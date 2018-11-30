# pylint: disable=redefined-outer-name,invalid-name

import decimal

import pytest

import sqlpuzzle
from sqlpuzzle._queryparts import Values


@pytest.fixture
def values():
    return Values()


def test_is_not_set(values):
    assert not values.is_set


def test_is_set(values):
    values.set(id=23)
    assert values.is_set


def test_values_by_tuple(values):
    values.set((
        ('name', 'Harry'),
        ('sex', 'female'),
        ('age', 20),
        ('country', None),
    ))
    assert str(values) == '"name" = \'Harry\', "sex" = \'female\', "age" = 20, "country" = NULL'


def test_values_by_list(values):
    values.set([
        ['name', 'Harry'],
        ['sex', 'female'],
        ['age', 20],
        ['country', None],
    ])
    assert str(values) == '"name" = \'Harry\', "sex" = \'female\', "age" = 20, "country" = NULL'


def test_values_by_dictionary(values):
    values.set({
        'name': 'Alan',
        'age': 20,
    })
    assert str(values) == '"age" = 20, "name" = \'Alan\''


def test_values_by_args(values):
    values.set('age', 20)
    assert str(values) == '"age" = 20'


def test_values_by_kwargs(values):
    values.set(name='Alan')
    assert str(values) == '"name" = \'Alan\''


def test_str(values):
    values.set(name='ščřž')
    assert str(values) == '"name" = \'ščřž\''


def test_custom_simple(values):
    customsql = sqlpuzzle.customsql('"age" = "age" + 1')
    values.set(customsql)
    assert str(values) == '"age" = "age" + 1'


def test_value_as_integer(values):
    values.set('col', 42)
    assert str(values) == '"col" = 42'


def test_value_as_float(values):
    values.set('col', 42.1)
    assert str(values) == '"col" = 42.10000'


def test_value_as_decimal(values):
    values.set('col', decimal.Decimal('42.1'))
    assert str(values) == '"col" = 42.10000'


def test_value_as_boolean(values):
    values.set('col', True)
    assert str(values) == '"col" = 1'


def test_value_as_bytes(values):
    values.set('col', b'data')
    assert str(values) == '"col" = x\'64617461\''


def test_value_as_bytes_postgresql(values, postgresql):
    values.set('col', b'data')
    assert str(values) == '"col" = E\'\\\\x64617461\''


def test_copy(values):
    values.set({'id': 42})
    copy = values.copy()
    values.set({'name': 'Alan'})
    assert str(copy) == '"id" = 42'
    assert str(values) == '"id" = 42, "name" = \'Alan\''


def test_equals(values):
    values.set({'id': 42})
    copy = values.copy()
    assert values == copy


def test_not_equals(values):
    values.set({'id': 42})
    copy = values.copy()
    values.set({'name': 'Alan'})
    assert not values == copy


def test_column_as_integer_exception(values):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        values.set(42, 'val')


def test_column_as_float_exception(values):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        values.set(42.1, 'val')


def test_column_as_boolean_exception(values):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        values.set(True, 'val')
