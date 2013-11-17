# -*- coding: utf-8 -*-

import six

import unittest

from sqlpuzzle.exceptions import InvalidArgumentException
from sqlpuzzle._queryparts import OrderBy


class OrderByTest(unittest.TestCase):
    def setUp(self):
        self.order_by = OrderBy()


class BaseTest(OrderByTest):
    def test_is_not_set(self):
        self.assertEqual(self.order_by.is_set, False)

    def test_is_set(self):
        self.order_by.order_by('id')
        self.assertEqual(self.order_by.is_set, True)

    def test_simply(self):
        self.order_by.order_by('id')
        self.assertEqual(str(self.order_by), 'ORDER BY "id"')

    def test_more_columns(self):
        self.order_by.order_by('id', ['name', 'desc'])
        self.assertEqual(str(self.order_by), 'ORDER BY "id", "name" DESC')

    def test_asc(self):
        self.order_by.order_by(['name', 'asc'])
        self.assertEqual(str(self.order_by), 'ORDER BY "name"')

    def test_desc(self):
        self.order_by.order_by(['name', 'desc'])
        self.assertEqual(str(self.order_by), 'ORDER BY "name" DESC')

    def test_order_by_number(self):
        self.order_by.order_by(1)
        self.assertEqual(str(self.order_by), 'ORDER BY 1')

    def test_by_dictionary(self):
        self.order_by.order_by({'id': 'ASC', 'name': 'DESC'})
        self.assertEqual(str(self.order_by), 'ORDER BY "id", "name" DESC')

    def test_by_kwds(self):
        self.order_by.order_by(id='ASC', name='DESC')
        self.assertEqual(str(self.order_by), 'ORDER BY "id", "name" DESC')

    def test_str(self):
        self.order_by.order_by('ščřž')
        self.assertEqual(str(self.order_by), 'ORDER BY "ščřž"')

    def test_unicode(self):
        if six.PY3:
            name = 'ščřž'
        else:
            name = unicode('ščřž', 'utf-8')
        self.order_by.order_by(name)
        self.assertEqual(str(self.order_by), 'ORDER BY "ščřž"')


class BackQuotesTest(OrderByTest):
    def test_column_name_as_table_and_column(self):
        self.order_by.order_by('table.column')
        self.assertEqual(str(self.order_by), 'ORDER BY "table"."column"')

    def test_column_name_as_table_and_column_with_dot_in_name(self):
        self.order_by.order_by('table."column."')
        self.assertEqual(str(self.order_by), 'ORDER BY "table"."column."')


class GroupingTest(OrderByTest):
    def test_more_same_columns_print_as_one(self):
        self.order_by.order_by('col', 'col')
        self.assertEqual(str(self.order_by), 'ORDER BY "col"')

    def test_more_same_columns_with_diff_asc_print_as_one(self):
        self.order_by.order_by('col', ('col', 'DESC'))
        self.assertEqual(str(self.order_by), 'ORDER BY "col" DESC')


class CopyTest(OrderByTest):
    def test_copy(self):
        self.order_by.order_by('name')
        copy = self.order_by.copy()
        self.order_by.order_by('surname')
        self.assertEqual(str(copy), 'ORDER BY "name"')
        self.assertEqual(str(self.order_by), 'ORDER BY "name", "surname"')

    def test_equals(self):
        self.order_by.order_by('name')
        copy = self.order_by.copy()
        self.assertTrue(self.order_by == copy)

    def test_not_equals(self):
        self.order_by.order_by('name')
        copy = self.order_by.copy()
        self.order_by.order_by('surname')
        self.assertFalse(self.order_by == copy)


class ExceptionsTest(OrderByTest):
    def test_name_as_float_exception(self):
        self.assertRaises(InvalidArgumentException, self.order_by.order_by, 42.1)

    def test_name_as_boolean_exception(self):
        self.assertRaises(InvalidArgumentException, self.order_by.order_by, True)

    def test_not_asc_or_desc_exception(self):
        self.assertRaises(InvalidArgumentException, self.order_by.order_by, ('col', 'AAA'))
