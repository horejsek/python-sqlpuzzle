# -*- coding: utf-8 -*-

import six

import unittest

import sqlpuzzle
from sqlpuzzle import Q
from sqlpuzzle._queryparts import Having


class HavingTest(unittest.TestCase):
    def setUp(self):
        self.having = Having()


class BaseTest(HavingTest):
    def test_is_not_set(self):
        self.assertEqual(self.having.is_set, False)

    def test_is_set(self):
        self.having.where(name='Alan')
        self.assertEqual(self.having.is_set, True)

    def test_where_by_tuple(self):
        self.having.where((
            ('name', 'Harry'),
            ('sex', sqlpuzzle.relations.NE('female')),
            ('age', sqlpuzzle.relations.GT(20)),
        ))
        self.assertEqual(str(self.having), 'HAVING "name" = \'Harry\' AND "sex" != \'female\' AND "age" > 20')

    def test_where_by_list(self):
        self.having.where([
            ['name', sqlpuzzle.relations.LIKE('Harry')],
            ['sex', sqlpuzzle.relations.NE('female')],
            ['age', sqlpuzzle.relations.LE(20)],
        ])
        self.assertEqual(str(self.having), 'HAVING "name" LIKE \'Harry\' AND "sex" != \'female\' AND "age" <= 20')

    def test_where_by_dictionary(self):
        self.having.where({
            'name': 'Alan',
            'age': 20,
        })
        self.assertEqual(str(self.having), 'HAVING "age" = 20 AND "name" = \'Alan\'')

    def test_where_by_args(self):
        self.having.where('age', sqlpuzzle.relations.LT(20))
        self.assertEqual(str(self.having), 'HAVING "age" < 20')

    def test_where_by_kwargs(self):
        self.having.where(name='Alan')
        self.assertEqual(str(self.having), 'HAVING "name" = \'Alan\'')

    def test_serial_where(self):
        self.having.where(name='Alan')
        self.having.where(age=42)
        self.assertEqual(str(self.having), 'HAVING "name" = \'Alan\' AND "age" = 42')

    def test_str(self):
        self.having.where(name='ščřž')
        self.assertEqual(str(self.having), 'HAVING "name" = \'ščřž\'')

    def test_unicode(self):
        if six.PY3:
            name = 'ščřž'
        else:
            name = unicode('ščřž', 'utf-8')
        self.having.where(name=name)
        self.assertEqual(str(self.having), 'HAVING "name" = \'ščřž\'')


class GroupingTest(HavingTest):
    def test_more_same_conditions_print_as_one(self):
        self.having.where(('age', 20), ('age', 20))
        self.assertEqual(str(self.having), 'HAVING "age" = 20')

    def test_more_same_conditions_with_diff_relation_print_as_more(self):
        self.having.where(('age', 20), ('age', sqlpuzzle.relations.NE(20)))
        self.assertEqual(str(self.having), 'HAVING "age" = 20 AND "age" != 20')


class CopyTest(HavingTest):
    def test_copy(self):
        self.having.where({'id': 42})
        copy = self.having.copy()
        self.having.where({'name': 'Alan'})
        self.assertEqual(str(copy), 'HAVING "id" = 42')
        self.assertEqual(str(self.having), 'HAVING "id" = 42 AND "name" = \'Alan\'')

    def test_equals(self):
        self.having.where({'id': 42})
        copy = self.having.copy()
        self.assertTrue(self.having == copy)

    def test_not_equals(self):
        self.having.where({'id': 42})
        copy = self.having.copy()
        self.having.where({'name': 'Alan'})
        self.assertFalse(self.having == copy)


class AllowedValuesTest(HavingTest):
    def test_value_as_integer(self):
        self.having.where('col', 42)
        self.assertEqual(str(self.having), 'HAVING "col" = 42')

    def test_value_as_float(self):
        self.having.where('col', 42.1)
        self.assertEqual(str(self.having), 'HAVING "col" = 42.10000')

    def test_value_as_boolean(self):
        self.having.where('col', True)
        self.assertEqual(str(self.having), 'HAVING "col" = 1')

    def test_value_as_list(self):
        self.having.where(id=(23, 34, 45))
        self.assertEqual(str(self.having), 'HAVING "id" IN (23, 34, 45)')

    def test_value_as_list_not_in(self):
        self.having.where('id', sqlpuzzle.relations.NOT_IN(23, 34, 45))
        self.assertEqual(str(self.having), 'HAVING "id" NOT IN (23, 34, 45)')


class ExceptionsTest(HavingTest):
    def test_column_as_integer_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 42, 'val')

    def test_column_as_float_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 42.1, 'val')

    def test_column_as_boolean_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, True, 'val')


class QObjectTest(HavingTest):
    def test_simple_or(self):
        self.having.where(Q(x='y') | Q(y='x'))
        self.assertEqual(str(self.having), 'HAVING ("x" = \'y\' OR "y" = \'x\')')

    def test_simple_and(self):
        self.having.where(Q(x='y') & Q(y='x'))
        self.assertEqual(str(self.having), 'HAVING ("x" = \'y\' AND "y" = \'x\')')

    def test_more_complicated(self):
        self.having.where((Q(a=1) & Q(b=2)) | Q(c=3))
        self.assertEqual(str(self.having), 'HAVING (("a" = 1 AND "b" = 2) OR "c" = 3)')

    def test_more_conditions_in_q(self):
        self.having.where(Q(a=42, b=24) | Q(x='y'))
        self.assertEqual(str(self.having), 'HAVING (("a" = 42 AND "b" = 24) OR "x" = \'y\')')
