# -*- coding: utf-8 -*-

import unittest

import six

import sqlpuzzle.exceptions
import sqlpuzzle._queries.delete


class DeleteTest(unittest.TestCase):
    def setUp(self):
        self.delete = sqlpuzzle._queries.delete.Delete()


class BaseTest(DeleteTest):
    def test_simply(self):
        self.delete.from_('user')
        self.delete.allow_delete_all()
        self.assertEqual(str(self.delete), 'DELETE FROM "user"')

    def test_str(self):
        self.delete.from_('user')
        self.delete.where(name='ščřž')
        self.assertEqual(str(self.delete), 'DELETE FROM "user" WHERE "name" = \'ščřž\'')

    def test_unicode(self):
        if six.PY3:
            name = 'ščřž'
        else:
            name = unicode('ščřž', 'utf-8')
        self.delete.from_('user')
        self.delete.where(name=name)
        self.assertEqual(str(self.delete), 'DELETE FROM "user" WHERE "name" = \'ščřž\'')


class PropertiesTest(DeleteTest):
    def test_has_not_references(self):
        self.assertFalse(self.delete.has('references'))

    def test_has_references(self):
        self.delete.from_('user')
        self.assertTrue(self.delete.has('references'))
        self.assertTrue(self.delete.has('references', 'user'))

    def test_has_not_where(self):
        self.assertFalse(self.delete.has('where'))

    def test_has_where(self):
        self.delete.where(id=1)
        self.assertTrue(self.delete.has('where'))
        self.assertTrue(self.delete.has('where', 'id'))


class MoreReferencesTest(DeleteTest):
    def setUp(self):
        super(MoreReferencesTest, self).setUp()
        self.delete.allow_delete_all()

    def test_more_tables(self):
        self.delete.delete('user').from_('user', 'user2')
        self.assertEqual(str(self.delete), 'DELETE "user" FROM "user", "user2"')

    def test_more_tables_with_alias(self):
        self.delete.delete('u').from_({'user': 'u', 'user2': 'u2'})
        self.assertEqual(str(self.delete), 'DELETE "u" FROM "user" AS "u", "user2" AS "u2"')

    def test_join(self):
        self.delete.delete('user').from_('user').left_join('role').on('role.id', 'user.role_id').where('role.name', ('a', 'b'))
        self.assertEqual(str(self.delete), 'DELETE "user" FROM "user" LEFT JOIN "role" ON "role"."id" = "user"."role_id" WHERE "role"."name" IN (\'a\', \'b\')')


class WhereTest(DeleteTest):
    def test_where(self):
        self.delete.from_('user')
        self.delete.where(age=42)
        self.delete.where('name', sqlpuzzle.relations.LIKE('Harry'))
        self.delete.where({
            'sex': 'male',
        })
        self.delete.where((
            ('enabled', 1),
        ))
        self.assertEqual(str(self.delete), 'DELETE FROM "user" WHERE "age" = 42 AND "name" LIKE \'Harry\' AND "sex" = \'male\' AND "enabled" = 1')


class CopyTest(DeleteTest):
    def test_copy(self):
        self.delete.from_('user').where(id=42)
        copy = self.delete.copy()
        self.delete.where(name='Harry')
        self.assertEqual(str(copy), 'DELETE FROM "user" WHERE "id" = 42')
        self.assertEqual(str(self.delete), 'DELETE FROM "user" WHERE "id" = 42 AND "name" = \'Harry\'')

    def test_equals(self):
        self.delete.from_('user').where(id=42)
        copy = self.delete.copy()
        self.assertTrue(self.delete == copy)

    def test_not_equals(self):
        self.delete.from_('user').where(id=42)
        copy = self.delete.copy()
        self.delete.where(name='Harry')
        self.assertFalse(self.delete == copy)


class DeleteOptionsTest(DeleteTest):
    def test_sql_cache(self):
        self.delete.from_('table').where(id=1).ignore()
        self.assertEqual(str(self.delete), 'DELETE IGNORE FROM "table" WHERE "id" = 1')
