
import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._features.columns


class ColumnsTest(unittest.TestCase):
    def setUp(self):
        self.columns = sqlpuzzle._features.columns.Columns()


class BaseTest(ColumnsTest):
    def test_is_not_set(self):
        self.assertEqual(self.columns.is_set(), False)

    def test_is_set(self):
        self.columns.columns('id')
        self.assertEqual(self.columns.is_set(), True)

    def test_one_column(self):
        self.columns.columns('id')
        self.assertEqual(str(self.columns), '`id`')

    def test_more_columns(self):
        self.columns.columns('id', 'name')
        self.assertEqual(str(self.columns), '`id`, `name`')

    def test_all_columns(self):
        self.assertEqual(str(self.columns), '*')

    def test_column_as(self):
        self.columns.columns(('id', 'ID'), 'name')
        self.assertEqual(str(self.columns), '`id` AS `ID`, `name`')

    def test_column_as_by_dictionary(self):
        self.columns.columns({'id': 'ID', 'name': 'Name'})
        self.assertEqual(str(self.columns), '`id` AS `ID`, `name` AS `Name`')

    def test_column_as_by_kwds(self):
        self.columns.columns(id='ID', name='Name')
        self.assertEqual(str(self.columns), '`id` AS `ID`, `name` AS `Name`')


class CustomSqlTest(ColumnsTest):
    def setUp(self):
        super(CustomSqlTest, self).setUp()
        self.customsql = sqlpuzzle.customsql('AVG(`custom`) AS `x`')

    def test_one_column(self):
        self.columns.columns(self.customsql)
        self.assertEqual(str(self.columns), 'AVG(`custom`) AS `x`')

    def test_more_columns(self):
        self.columns.columns(self.customsql, 'id')
        self.assertEqual(str(self.columns), 'AVG(`custom`) AS `x`, `id`')

    def test_custom_in_column_with_as(self):
        self.columns.columns({sqlpuzzle.customsql('AVG(`custom`)'): 'x'})
        self.assertEqual(str(self.columns), 'AVG(`custom`) AS `x`')


class BackQuotesTest(ColumnsTest):
    def test_column_name_as_table_and_column(self):
        self.columns.columns('table.column')
        self.assertEqual(str(self.columns), '`table`.`column`')

    def test_column_name_as_table_and_column_with_dot_in_name(self):
        self.columns.columns('table.`column.`')
        self.assertEqual(str(self.columns), '`table`.`column.`')


class GroupingTest(ColumnsTest):
    def test_more_same_columns_print_as_one(self):
        self.columns.columns('col', 'col')
        self.assertEqual(str(self.columns), '`col`')

    def test_more_same_columns_with_diff_as_print_as_more(self):
        self.columns.columns('col', ('col', 'col2'))
        self.assertEqual(str(self.columns), '`col`, `col` AS `col2`')


class CopyTest(ColumnsTest):
    def test_copy(self):
        self.columns.columns('id', 'name')
        copy = self.columns.copy()
        self.columns.columns('address')
        self.assertEqual(str(copy), '`id`, `name`')
        self.assertEqual(str(self.columns), '`id`, `name`, `address`')

    def test_equals(self):
        self.columns.columns('id', 'name')
        copy = self.columns.copy()
        self.assertTrue(self.columns == copy)

    def test_not_equals(self):
        self.columns.columns('id', 'name')
        copy = self.columns.copy()
        self.columns.columns('address')
        self.assertFalse(self.columns == copy)


class ExceptionsTest(ColumnsTest):
    def test_name_as_float_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.columns.columns, 42.1)

    def test_name_as_boolean_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.columns.columns, True)
