# pylint: disable=redefined-outer-name,invalid-name

import pytest

import sqlpuzzle
from sqlpuzzle._queryparts import GroupBy


@pytest.fixture
def group_by():
    return GroupBy()


def test_is_not_set(group_by):
    assert not group_by.is_set


def test_is_set(group_by):
    group_by.group_by('id')
    assert group_by.is_set


def test_simply(group_by):
    group_by.group_by('id')
    assert str(group_by) == 'GROUP BY "id"'


def test_more_columns(group_by):
    group_by.group_by('id', ['name', 'desc'])
    assert str(group_by) == 'GROUP BY "id", "name" DESC'


def test_asc(group_by):
    group_by.group_by(['name', 'asc'])
    assert str(group_by) == 'GROUP BY "name"'


def test_desc(group_by):
    group_by.group_by(['name', 'desc'])
    assert str(group_by) == 'GROUP BY "name" DESC'


def test_order_by_number(group_by):
    group_by.group_by(1)
    assert str(group_by) == 'GROUP BY 1'


def test_by_dictionary(group_by):
    group_by.group_by({'id': 'ASC', 'name': 'DESC'})
    assert str(group_by) == 'GROUP BY "id", "name" DESC'


def test_by_kwds(group_by):
    group_by.group_by(id='ASC', name='DESC')
    assert str(group_by) == 'GROUP BY "id", "name" DESC'


def test_str(group_by):
    group_by.group_by('ščřž')
    assert str(group_by) == 'GROUP BY "ščřž"'


def test_column_name_as_table_and_column(group_by):
    group_by.group_by('table.column')
    assert str(group_by) == 'GROUP BY "table"."column"'


def test_column_name_as_table_and_column_with_dot_in_name(group_by):
    group_by.group_by('table."column."')
    assert str(group_by) == 'GROUP BY "table"."column."'


def test_more_same_columns_print_as_one(group_by):
    group_by.group_by('col', 'col')
    assert str(group_by) == 'GROUP BY "col"'


def test_more_same_columns_with_diff_asc_print_as_one(group_by):
    group_by.group_by('col', ('col', 'DESC'))
    assert str(group_by) == 'GROUP BY "col" DESC'


def test_copy(group_by):
    group_by.group_by('id', 'name')
    copy = group_by.copy()
    group_by.group_by('address')
    assert str(copy) == 'GROUP BY "id", "name"'
    assert str(group_by) == 'GROUP BY "id", "name", "address"'


def test_equals(group_by):
    group_by.group_by('id', 'name')
    copy = group_by.copy()
    assert group_by == copy


def test_not_equals(group_by):
    group_by.group_by('id', 'name')
    copy = group_by.copy()
    group_by.group_by('address')
    assert not group_by == copy


def test_name_as_float_exception(group_by):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        group_by.group_by(42.1)


def test_name_as_boolean_exception(group_by):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        group_by.group_by(True)


def test_not_asc_or_desc_exception(group_by):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        group_by.group_by(('col', 'AAA'))
