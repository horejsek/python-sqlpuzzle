# -*- coding: utf-8 -*-

import six

import unittest

import sqlpuzzle
from sqlpuzzle._queryparts import Values


class ValuesTest(unittest.TestCase):
    def setUp(self):
        self.values = Values()


class BaseTest(ValuesTest):
    def test_is_not_set(self):
        self.assertEqual(self.values.is_set(), False)

    def test_is_set(self):
        self.values.set(id=23)
        self.assertEqual(self.values.is_set(), True)

    def test_values_by_tuple(self):
        self.values.set((
            ('name', 'Harry'),
            ('sex', 'female'),
            ('age', 20),
            ('country', None),
        ))
        self.assertEqual(str(self.values), '`name` = "Harry", `sex` = "female", `age` = 20, `country` = NULL')

    def test_values_by_list(self):
        self.values.set([
            ['name', 'Harry'],
            ['sex', 'female'],
            ['age', 20],
            ['country', None],
        ])
        self.assertEqual(str(self.values), '`name` = "Harry", `sex` = "female", `age` = 20, `country` = NULL')

    def test_values_by_dictionary(self):
        self.values.set({
            'name': 'Alan',
            'age': 20,
        })
        self.assertEqual(str(self.values), '`age` = 20, `name` = "Alan"')

    def test_values_by_args(self):
        self.values.set('age', 20)
        self.assertEqual(str(self.values), '`age` = 20')

    def test_values_by_kwargs(self):
        self.values.set(name='Alan')
        self.assertEqual(str(self.values), '`name` = "Alan"')

    def test_str(self):
        self.values.set(name='ščřž')
        self.assertEqual(str(self.values), '`name` = "ščřž"')

    def test_unicode(self):
        if six.PY3:
            name = 'ščřž'
        else:
            name = unicode('ščřž', 'utf-8')
        self.values.set(name=name)
        self.assertEqual(str(self.values), '`name` = "ščřž"')


class CustomSqlTest(ValuesTest):
    def setUp(self):
        super(CustomSqlTest, self).setUp()
        self.customsql = sqlpuzzle.customsql('`age` = `age` + 1')

    def test_simple(self):
        self.values.set(self.customsql)
        self.assertEqual(str(self.values), '`age` = `age` + 1')


class AllowedValuesTest(ValuesTest):
    def test_value_as_integer(self):
        self.values.set('col', 42)
        self.assertEqual(str(self.values), '`col` = 42')

    def test_value_as_float(self):
        self.values.set('col', 42.1)
        self.assertEqual(str(self.values), '`col` = 42.10000')

    def test_value_as_boolean(self):
        self.values.set('col', True)
        self.assertEqual(str(self.values), '`col` = 1')


class CopyTest(ValuesTest):
    def test_copy(self):
        self.values.set({'id': 42})
        copy = self.values.copy()
        self.values.set({'name': 'Alan'})
        self.assertEqual(str(copy), '`id` = 42')
        self.assertEqual(str(self.values), '`id` = 42, `name` = "Alan"')

    def test_equals(self):
        self.values.set({'id': 42})
        copy = self.values.copy()
        self.assertTrue(self.values == copy)

    def test_not_equals(self):
        self.values.set({'id': 42})
        copy = self.values.copy()
        self.values.set({'name': 'Alan'})
        self.assertFalse(self.values == copy)


class ExceptionsTest(ValuesTest):
    def test_column_as_integer_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.values.set, 42, 'val')

    def test_column_as_float_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.values.set, 42.1, 'val')

    def test_column_as_boolean_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.values.set, True, 'val')
