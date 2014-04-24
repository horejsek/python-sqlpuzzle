# -*- coding: utf-8 -*-

import unittest

import six

import sqlpuzzle.exceptions
import sqlpuzzle._queries.insert


class InsertTest(unittest.TestCase):
    def setUp(self):
        self.insert = sqlpuzzle._queries.insert.Insert()


class BaseTest(InsertTest):
    def test_simply(self):
        self.insert.into('user')
        self.insert.values(name='Alan')
        self.assertEqual(str(self.insert), 'INSERT INTO "user" ("name") VALUES (\'Alan\')')

    def test_str(self):
        self.insert.into('user')
        self.insert.values(name='ščřž')
        self.assertEqual(str(self.insert), 'INSERT INTO "user" ("name") VALUES (\'ščřž\')')

    def test_unicode(self):
        if six.PY3:
            name = 'ščřž'
        else:
            name = unicode('ščřž', 'utf-8')
        self.insert.into('user')
        self.insert.values(name=name)
        self.assertEqual(str(self.insert), 'INSERT INTO "user" ("name") VALUES (\'ščřž\')')


class PropertiesTest(InsertTest):
    def test_has_not_tables(self):
        self.assertFalse(self.insert.has('tables'))

    def test_has_tables(self):
        self.insert.into('user')
        self.assertTrue(self.insert.has('tables'))
        self.assertTrue(self.insert.has('tables', 'user'))

    def test_has_not_values(self):
        self.assertFalse(self.insert.has('values'))

    def test_has_values(self):
        self.insert.values(id=1)
        self.assertTrue(self.insert.has('values'))
        self.assertTrue(self.insert.has('values', '1'))


class OnDuplicateKeyUpdateTest(InsertTest):
    def test_on_duplicate_key_update(self):
        self.insert.into('user')
        values = {
            'name': 'Alan',
        }
        self.insert.values(id=1, **values)
        self.insert.on_duplicate_key_update(values)
        self.assertEqual(str(self.insert), 'INSERT INTO "user" ("id", "name") VALUES (1, \'Alan\') ON DUPLICATE KEY UPDATE "name" = \'Alan\'')


class CopyTest(InsertTest):
    def test_copy(self):
        self.insert.into('user').values(id=1)
        copy = self.insert.copy()
        self.insert.values(id=2)
        self.assertEqual(str(copy), 'INSERT INTO "user" ("id") VALUES (1)')
        self.assertEqual(str(self.insert), 'INSERT INTO "user" ("id") VALUES (1), (2)')

    def test_equals(self):
        self.insert.into('user').values(id=1)
        copy = self.insert.copy()
        self.assertTrue(self.insert == copy)

    def test_not_equals(self):
        self.insert.into('user').values(id=1)
        copy = self.insert.copy()
        self.insert.values(name='Alan')
        self.assertFalse(self.insert == copy)


class MultipleInsertTest(InsertTest):
    def test(self):
        self.insert.into('table').values(id=1).values(id=2).values(id=3)
        self.assertEqual(str(self.insert), 'INSERT INTO "table" ("id") VALUES (1), (2), (3)')
