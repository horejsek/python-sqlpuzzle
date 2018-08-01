# pylint: disable=redefined-outer-name,invalid-name

import pytest

from sqlpuzzle.exceptions import InvalidArgumentException
from sqlpuzzle._queryparts import OrderBy


@pytest.fixture
def order_by():
    return OrderBy()


def test_is_not_set(order_by):
    assert not order_by.is_set


def test_is_set(order_by):
    order_by.order_by('id')
    assert order_by.is_set


def test_simply(order_by):
    order_by.order_by('id')
    assert str(order_by) == 'ORDER BY "id"'


def test_more_columns(order_by):
    order_by.order_by('id', ['name', 'desc'])
    assert str(order_by) == 'ORDER BY "id", "name" DESC'


def test_asc(order_by):
    order_by.order_by(['name', 'asc'])
    assert str(order_by) == 'ORDER BY "name"'


def test_desc(order_by):
    order_by.order_by(['name', 'desc'])
    assert str(order_by) == 'ORDER BY "name" DESC'


def test_order_by_number(order_by):
    order_by.order_by(1)
    assert str(order_by) == 'ORDER BY 1'


def test_by_dictionary(order_by):
    order_by.order_by({'id': 'ASC', 'name': 'DESC'})
    assert str(order_by) == 'ORDER BY "id", "name" DESC'


def test_by_kwds(order_by):
    order_by.order_by(id='ASC', name='DESC')
    assert str(order_by) == 'ORDER BY "id", "name" DESC'


def test_str(order_by):
    order_by.order_by('ščřž')
    assert str(order_by) == 'ORDER BY "ščřž"'


def test_column_name_as_table_and_column(order_by):
    order_by.order_by('table.column')
    assert str(order_by) == 'ORDER BY "table"."column"'


def test_column_name_as_table_and_column_with_dot_in_name(order_by):
    order_by.order_by('table."column."')
    assert str(order_by) == 'ORDER BY "table"."column."'


def test_more_same_columns_print_as_one(order_by):
    order_by.order_by('col', 'col')
    assert str(order_by) == 'ORDER BY "col"'


def test_more_same_columns_with_diff_asc_print_as_one(order_by):
    order_by.order_by('col', ('col', 'DESC'))
    assert str(order_by) == 'ORDER BY "col" DESC'


def test_copy(order_by):
    order_by.order_by('name')
    copy = order_by.copy()
    order_by.order_by('surname')
    assert str(copy) == 'ORDER BY "name"'
    assert str(order_by) == 'ORDER BY "name", "surname"'


def test_equals(order_by):
    order_by.order_by('name')
    copy = order_by.copy()
    assert order_by == copy


def test_not_equals(order_by):
    order_by.order_by('name')
    copy = order_by.copy()
    order_by.order_by('surname')
    assert not order_by == copy


def test_name_as_float_exception(order_by):
    with pytest.raises(InvalidArgumentException):
        order_by.order_by(42.1)


def test_name_as_boolean_exception(order_by):
    with pytest.raises(InvalidArgumentException):
        order_by.order_by(True)


def test_not_asc_or_desc_exception(order_by):
    with pytest.raises(InvalidArgumentException):
        order_by.order_by(('col', 'AAA'))
