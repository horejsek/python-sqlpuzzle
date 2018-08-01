# pylint: disable=redefined-outer-name,invalid-name

import pytest

import sqlpuzzle
from sqlpuzzle._queryparts import Columns


@pytest.fixture
def columns():
    return Columns()


def test_is_not_set(columns):
    assert columns.is_set


def test_is_set(columns):
    columns.columns('id')
    assert columns.is_set


def test_one_column(columns):
    columns.columns('id')
    assert str(columns) == '"id"'


def test_more_columns(columns):
    columns.columns('id', 'name')
    assert str(columns) == '"id", "name"'


def test_all_columns(columns):
    assert str(columns) == '*'


def test_column_as(columns):
    columns.columns(('id', 'ID'), 'name')
    assert str(columns) == '"id" AS "ID", "name"'


def test_column_as_by_dictionary(columns):
    columns.columns({'id': 'ID', 'name': 'Name'})
    assert str(columns) == '"id" AS "ID", "name" AS "Name"'


def test_column_as_by_kwds(columns):
    columns.columns(id='ID', name='Name')
    assert str(columns) == '"id" AS "ID", "name" AS "Name"'


def test_column_by_args_and_kwds(columns):
    columns.columns('id', name='Name')
    assert str(columns) == '"id", "name" AS "Name"'


def test_str(columns):
    columns.columns('ščřž')
    assert str(columns) == '"ščřž"'


def test_custom_one_column(columns):
    customsql = sqlpuzzle.customsql('AVG("custom") AS "x"')
    columns.columns(customsql)
    assert str(columns) == 'AVG("custom") AS "x"'


def test_custom_more_columns(columns):
    customsql = sqlpuzzle.customsql('AVG("custom") AS "x"')
    columns.columns(customsql, 'id')
    assert str(columns) == 'AVG("custom") AS "x", "id"'


def test_custom_in_column_with_as(columns):
    columns.columns({sqlpuzzle.customsql('AVG("custom")'): 'x'})
    assert str(columns) == 'AVG("custom") AS "x"'


def test_column_name_as_table_and_column(columns):
    columns.columns('table.column')
    assert str(columns) == '"table"."column"'


def test_column_name_as_table_and_column_with_dot_in_name(columns):
    columns.columns('table."column."')
    assert str(columns) == '"table"."column."'


def test_more_same_columns_print_as_one(columns):
    columns.columns('col', 'col')
    assert str(columns) == '"col"'


def test_more_same_columns_with_diff_as_print_as_more(columns):
    columns.columns('col', ('col', 'col2'))
    assert str(columns) == '"col", "col" AS "col2"'


def test_copy(columns):
    columns.columns('id', 'name')
    copy = columns.copy()
    columns.columns('address')
    assert str(copy) == '"id", "name"'
    assert str(columns) == '"id", "name", "address"'


def test_equals(columns):
    columns.columns('id', 'name')
    copy = columns.copy()
    assert columns == copy


def test_not_equals(columns):
    columns.columns('id', 'name')
    copy = columns.copy()
    columns.columns('address')
    assert not columns == copy


def test_name_as_float_exception(columns):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        columns.columns(42.1)


def test_name_as_boolean_exception(columns):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        columns.columns(True)
