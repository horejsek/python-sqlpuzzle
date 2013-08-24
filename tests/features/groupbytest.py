# -*- coding: utf-8 -*-

import unittest

import sqlpuzzle
from sqlpuzzle._queryparts import GroupBy


class GroupByTest(unittest.TestCase):
    def setUp(self):
        self.group_by = GroupBy()


class BaseTest(GroupByTest):
    def test_is_not_set(self):
        self.assertEqual(self.group_by.is_set(), False)

    def test_is_set(self):
        self.group_by.group_by('id')
        self.assertEqual(self.group_by.is_set(), True)

    def test_simply(self):
        self.group_by.group_by('id')
        self.assertEqual(str(self.group_by), 'GROUP BY `id`')

    def test_more_columns(self):
        self.group_by.group_by('id', ['name', 'desc'])
        self.assertEqual(str(self.group_by), 'GROUP BY `id`, `name` DESC')

    def test_asc(self):
        self.group_by.group_by(['name', 'asc'])
        self.assertEqual(str(self.group_by), 'GROUP BY `name`')

    def test_desc(self):
        self.group_by.group_by(['name', 'desc'])
        self.assertEqual(str(self.group_by), 'GROUP BY `name` DESC')

    def test_order_by_number(self):
        self.group_by.group_by(1)
        self.assertEqual(str(self.group_by), 'GROUP BY 1')

    def test_by_dictionary(self):
        self.group_by.group_by({'id': 'ASC', 'name': 'DESC'})
        self.assertEqual(str(self.group_by), 'GROUP BY `id`, `name` DESC')

    def test_by_kwds(self):
        self.group_by.group_by(id='ASC', name='DESC')
        self.assertEqual(str(self.group_by), 'GROUP BY `id`, `name` DESC')


class BackQuotesTest(GroupByTest):
    def test_column_name_as_table_and_column(self):
        self.group_by.group_by('table.column')
        self.assertEqual(str(self.group_by), 'GROUP BY `table`.`column`')

    def test_column_name_as_table_and_column_with_dot_in_name(self):
        self.group_by.group_by('table.`column.`')
        self.assertEqual(str(self.group_by), 'GROUP BY `table`.`column.`')


class GroupingTest(GroupByTest):
    def test_more_same_columns_print_as_one(self):
        self.group_by.group_by('col', 'col')
        self.assertEqual(str(self.group_by), 'GROUP BY `col`')

    def test_more_same_columns_with_diff_asc_print_as_one(self):
        self.group_by.group_by('col', ('col', 'DESC'))
        self.assertEqual(str(self.group_by), 'GROUP BY `col` DESC')


class CopyTest(GroupByTest):
    def test_copy(self):
        self.group_by.group_by('id', 'name')
        copy = self.group_by.copy()
        self.group_by.group_by('address')
        self.assertEqual(str(copy), 'GROUP BY `id`, `name`')
        self.assertEqual(str(self.group_by), 'GROUP BY `id`, `name`, `address`')

    def test_equals(self):
        self.group_by.group_by('id', 'name')
        copy = self.group_by.copy()
        self.assertTrue(self.group_by == copy)

    def test_not_equals(self):
        self.group_by.group_by('id', 'name')
        copy = self.group_by.copy()
        self.group_by.group_by('address')
        self.assertFalse(self.group_by == copy)


class ExceptionsTest(GroupByTest):
    def test_name_as_float_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.group_by.group_by, 42.1)

    def test_name_as_boolean_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.group_by.group_by, True)

    def test_not_asc_or_desc_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.group_by.group_by, ('col', 'AAA'))
