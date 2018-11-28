# pylint: disable=invalid-name

import datetime
import decimal

import pytest

import sqlpuzzle
from sqlpuzzle._common import SqlValue, SqlReference


def test_string():
    assert str(SqlValue('Hello World!')) == '\'Hello World!\''


def test_integer():
    assert str(SqlValue(42)) == '42'


def test_long_integer():
    assert str(SqlValue(123456789012345)) == '123456789012345'


def test_float():
    assert str(SqlValue(23.456)) == '23.45600'


def test_decimal():
    assert str(SqlValue(decimal.Decimal('23.456'))) == '23.45600'


def test_boolean():
    assert str(SqlValue(True)) == '1'


def test_date():
    assert str(SqlValue(datetime.date(2011, 5, 25))) == '\'2011-05-25\''


def test_datetime():
    assert str(SqlValue(datetime.datetime(2011, 5, 25, 19, 33, 20))) == '\'2011-05-25T19:33:20\''


def test_list_with_string():
    assert str(SqlValue(['a', 'b', 'c'])) == "('a', 'b', 'c')"


def test_list_with_integer():
    assert str(SqlValue([12, 23, 34])) == '(12, 23, 34)'


def test_empty_list():
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        str(SqlValue([]))


def test_tuple_with_string():
    assert str(SqlValue(('a', 'b', 'c'))) == "('a', 'b', 'c')"


def test_tuple_with_integer():
    assert str(SqlValue((12, 23, 34))) == '(12, 23, 34)'


def test_empty_tuple():
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        str(SqlValue(()))


def test_set():
    assert str(SqlValue(set([12, 23]))) == '(12, 23)'


def test_empty_set():
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        str(SqlValue(set()))


def test_frozen_set():
    assert str(SqlValue(frozenset([12, 23]))) == '(12, 23)'


def test_empty_frozen_set():
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        str(SqlValue(frozenset()))


def test_generator():
    assert str(SqlValue(x for x in (12, 23, 34))) == '(12, 23, 34)'


def test_xrange():
    assert str(SqlValue(range(5))) == '(0, 1, 2, 3, 4)'


def test_none():
    assert str(SqlValue(None)) == 'NULL'


def test_subselect():
    select = sqlpuzzle.select_from('table')
    assert str(SqlValue(select)) == '(SELECT * FROM "table")'


def test_security_string():
    assert str(SqlReference('test')) == '"test"'


def test_security_subselect():
    select = sqlpuzzle.select_from('table')
    assert str(SqlReference(select)) == '(SELECT * FROM "table")'


def test_security_table_column():
    assert str(SqlReference('table.column')) == '"table"."column"'


def test_security_database_table_column():
    assert str(SqlReference('db.table.column')) == '"db"."table"."column"'


def test_security_single_quotes():
    assert str(SqlValue('test\'test')) == "'test''test'"


def test_security_quotes():
    assert str(SqlValue('test"test')) == "'test\"test'"


def test_security_slash():
    assert str(SqlValue('test\\test')) == "'test\\\\test'"


def test_new_line():
    value = """first line
second line"""
    assert str(SqlValue(value)) == "'first line\\nsecond line'"


def test_sqlreference_compare_to_str():
    assert SqlReference('foo') == '"foo"'
    assert SqlReference('foo') != 'foo'


def test_sqlvalue_compare_to_str():
    assert SqlValue('foo') == "'foo'"
    assert SqlValue('foo') != 'foo'
