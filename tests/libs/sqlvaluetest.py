
import six
from six.moves import xrange

import datetime
import unittest

import sqlpuzzle
from sqlpuzzle._common import SqlValue, SqlReference


class SqlValueTest(unittest.TestCase):
    def test_string(self):
        self.assertEqual(str(SqlValue('Hello World!')), '"Hello World!"')

    def test_unicode(self):
        self.assertEqual(str(SqlValue(six.u('Hello World!'))), '"Hello World!"')

    def test_integer(self):
        self.assertEqual(str(SqlValue(42)), '42')

    def test_long_integer(self):
        self.assertEqual(str(SqlValue(123456789012345)), '123456789012345')

    def test_float(self):
        self.assertEqual(str(SqlValue(23.456)), '23.45600')

    def test_boolean(self):
        self.assertEqual(str(SqlValue(True)), '1')

    def test_date(self):
        self.assertEqual(str(SqlValue(datetime.date(2011, 5, 25))), '"2011-05-25"')

    def test_datetime(self):
        self.assertEqual(str(SqlValue(datetime.datetime(2011, 5, 25, 19, 33, 20))), '"2011-05-25T19:33:20"')

    def test_list_with_string(self):
        self.assertEqual(str(SqlValue(['a', 'b', 'c'])), '("a", "b", "c")')

    def test_list_with_integer(self):
        self.assertEqual(str(SqlValue([12,23,34])), '(12, 23, 34)')

    def test_empty_list(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, str, SqlValue([]))

    def test_tuple_with_integer(self):
        self.assertEqual(str(SqlValue(('a', 'b', 'c'))), '("a", "b", "c")')

    def test_tuple_with_integer(self):
        self.assertEqual(str(SqlValue((12,23,34))), '(12, 23, 34)')

    def test_empty_tuple(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, str, SqlValue(()))

    def test_set(self):
        self.assertEqual(str(SqlValue(set([12, 23]))), '(12, 23)')

    def test_empty_set(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, str, SqlValue(set()))

    def test_frozen_set(self):
        self.assertEqual(str(SqlValue(frozenset([12, 23]))), '(12, 23)')

    def test_empty_frozen_set(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, str, SqlValue(frozenset()))

    def test_generator(self):
        self.assertEqual(str(SqlValue(x for x in (12, 23, 34))), '(12, 23, 34)')

    def test_xrange(self):
        self.assertEqual(str(SqlValue(xrange(5))), '(0, 1, 2, 3, 4)')

    def test_none(self):
        self.assertEqual(str(SqlValue(None)), 'NULL')

    def test_subselect(self):
        select = sqlpuzzle.select_from('table')
        self.assertEqual(str(SqlValue(select)), '(SELECT * FROM `table`)')


class SqlReferenceTest(unittest.TestCase):
    def test_string(self):
        self.assertEqual(str(SqlReference('test')), '`test`')

    def test_unicode(self):
        self.assertEqual(str(SqlReference(six.u('test'))), '`test`')

    def test_subselect(self):
        select = sqlpuzzle.select_from('table')
        self.assertEqual(str(SqlReference(select)), '(SELECT * FROM `table`)')

    def test_table_column(self):
        self.assertEqual(str(SqlReference('table.column')), '`table`.`column`')

    def test_database_table_column(self):
        self.assertEqual(str(SqlReference('db.table.column')), '`db`.`table`.`column`')


class SecurityTest(unittest.TestCase):
    def test_single_quotes(self):
        self.assertEqual(str(SqlValue('test\'test')), '"test\\\'test"')

    def test_quotes(self):
        self.assertEqual(str(SqlValue('test"test')), '"test\\"test"')

    def test_slash(self):
        self.assertEqual(str(SqlValue('test\\test')), '"test\\\\test"')

    def test_new_line(self):
        value = """first line
second line"""
        self.assertEqual(str(SqlValue(value)), '"first line\\nsecond line"')
