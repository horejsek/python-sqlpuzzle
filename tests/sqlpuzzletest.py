# -*- coding: utf-8 -*-

import unittest

import sqlpuzzle
from sqlpuzzle._common import SqlValue, SqlReference
from sqlpuzzle._queryparts import Column


class SqlPuzzleTest(unittest.TestCase):
    def test_select_test(self):
        sql = sqlpuzzle.select(1)
        self.assertEqual(str(sql), 'SELECT 1')

    def test_select_without_columns(self):
        sql = sqlpuzzle.select().from_('user')
        self.assertEqual(str(sql), 'SELECT * FROM "user"')

    def test_select_with_columns(self):
        sql = sqlpuzzle.select('id', 'name').from_('user')
        self.assertEqual(str(sql), 'SELECT "id", "name" FROM "user"')

    def test_select_from(self):
        sql = sqlpuzzle.select_from('user')
        self.assertEqual(str(sql), 'SELECT * FROM "user"')

    def test_select_from_as_kwds(self):
        sql = sqlpuzzle.select_from(user='u')
        self.assertEqual(str(sql), 'SELECT * FROM "user" AS "u"')

    def test_select_from_with_more(self):
        sql = sqlpuzzle.select_from('user', 'country')
        self.assertEqual(str(sql), 'SELECT * FROM "user", "country"')

    def test_insert(self):
        sql = sqlpuzzle.insert().into('user').values(name='Harry')
        self.assertEqual(str(sql), 'INSERT INTO "user" ("name") VALUES (\'Harry\')')

    def test_insert_into(self):
        sql = sqlpuzzle.insert_into('user').values(name='Harry')
        self.assertEqual(str(sql), 'INSERT INTO "user" ("name") VALUES (\'Harry\')')

    def test_update(self):
        sql = sqlpuzzle.update('user').set(name='Alan').where(id=42)
        self.assertEqual(str(sql), 'UPDATE "user" SET "name" = \'Alan\' WHERE "id" = 42')

    def test_delete(self):
        sql = sqlpuzzle.delete().from_('user').where(id=42)
        self.assertEqual(str(sql), 'DELETE FROM "user" WHERE "id" = 42')

    def test_delete_from(self):
        sql = sqlpuzzle.delete_from('user').where(id=42)
        self.assertEqual(str(sql), 'DELETE FROM "user" WHERE "id" = 42')


class CopyTest(unittest.TestCase):
    def test_copy1(self):
        query1 = sqlpuzzle.select_from('t').where('c', sqlpuzzle.relations.GT(1))
        query2 = query1.copy()
        self.assertEquals(str(query1), str(query2))

    def test_copy_with_custom(self):
        query1 = sqlpuzzle.select_from('t').where(sqlpuzzle.customsql('x'))
        query2 = query1.copy()
        self.assertEquals(str(query1), str(query2))


class CompareTest(unittest.TestCase):
    def test_compare_column_with_custom(self):
        custom = sqlpuzzle.customsql('custom')
        column = Column('column')
        self.assertFalse(column == custom)  # Do not throw exception.


class RelationTest(unittest.TestCase):
    def test_custom_sql(self):
        # Do not throw exception InvalidArgumentException.
        sqlpuzzle.relations.EQ(sqlpuzzle.customsql('custom'))
        sqlpuzzle.relations.NE(sqlpuzzle.customsql('custom'))
        sqlpuzzle.relations.GT(sqlpuzzle.customsql('custom'))
        sqlpuzzle.relations.GE(sqlpuzzle.customsql('custom'))
        sqlpuzzle.relations.LT(sqlpuzzle.customsql('custom'))
        sqlpuzzle.relations.LE(sqlpuzzle.customsql('custom'))
        sqlpuzzle.relations.LIKE(sqlpuzzle.customsql('custom'))
        sqlpuzzle.relations.REGEXP(sqlpuzzle.customsql('custom'))
        sqlpuzzle.relations.IN(sqlpuzzle.customsql('custom'))
        sqlpuzzle.relations.NOT_IN(sqlpuzzle.customsql('custom'))
        sqlpuzzle.relations.IS(sqlpuzzle.customsql('custom'))
        sqlpuzzle.relations.IS_NOT(sqlpuzzle.customsql('custom'))


class ShortcutsTest(unittest.TestCase):
    def test_sql_value(self):
        self.assertIsInstance(sqlpuzzle.V('5'), SqlValue)

    def test_sql_reference(self):
        self.assertIsInstance(sqlpuzzle.R('table'), SqlReference)
