# -*- coding: utf-8 -*-

import unittest

import six

import sqlpuzzle.exceptions
import sqlpuzzle._queries.update
import sqlpuzzle.relations


class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.update = sqlpuzzle._queries.update.Update()


class BaseTest(UpdateTest):
    def test_simply(self):
        self.update.table('user')
        self.update.set(name='Alan')
        self.update.allow_update_all()
        self.assertEqual(str(self.update), 'UPDATE "user" SET "name" = \'Alan\'')

    def test_str(self):
        self.update.table('user')
        self.update.set(name='ščřž')
        self.update.allow_update_all()
        self.assertEqual(str(self.update), 'UPDATE "user" SET "name" = \'ščřž\'')

    def test_unicode(self):
        if six.PY3:
            name = 'ščřž'
        else:
            name = unicode('ščřž', 'utf-8')
        self.update.table('user')
        self.update.set(name=name)
        self.update.allow_update_all()
        self.assertEqual(str(self.update), 'UPDATE "user" SET "name" = \'ščřž\'')


class WhereTest(UpdateTest):
    def test_where(self):
        self.update.table('user')
        self.update.set(name='Alan')
        self.update.where(age=42)
        self.update.where('name', sqlpuzzle.relations.LIKE('Harry'))
        self.update.where({
            'sex': 'male',
        })
        self.update.where((
            ('enabled', 1),
        ))
        self.assertEqual(str(self.update), 'UPDATE "user" SET "name" = \'Alan\' WHERE "age" = 42 AND "name" LIKE \'Harry\' AND "sex" = \'male\' AND "enabled" = 1')


class CopyTest(UpdateTest):
    def test_copy(self):
        self.update.table('user').set(name='Alan').where(id=42)
        copy = self.update.copy()
        self.update.set(age=24)
        self.assertEqual(str(copy), 'UPDATE "user" SET "name" = \'Alan\' WHERE "id" = 42')
        self.assertEqual(str(self.update), 'UPDATE "user" SET "name" = \'Alan\', "age" = 24 WHERE "id" = 42')

    def test_equals(self):
        self.update.table('user').set(name='Alan').where(id=42)
        copy = self.update.copy()
        self.assertTrue(self.update == copy)

    def test_not_equals(self):
        self.update.table('user').set(name='Alan').where(id=42)
        copy = self.update.copy()
        self.update.set(age=24)
        self.assertFalse(self.update == copy)
