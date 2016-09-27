# -*- coding: utf-8 -*-

import unittest

import sqlpuzzle


class SqliteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sqlpuzzle.configure('sqlite')

    @classmethod
    def tearDownClass(cls):
        sqlpuzzle.configure('sql')

    def test_reference(self):
        sql = sqlpuzzle.select('id').from_('table')
        self.assertEqual(str(sql), 'SELECT "id" FROM "table"')

    def test_boolean(self):
        sql = sqlpuzzle.select_from('table').where({'flag': True})
        self.assertEqual(str(sql), 'SELECT * FROM "table" WHERE "flag" = 1')

    def test_on_duplicate_key_update(self):
        sql = sqlpuzzle.insert_into('user')
        sql.values(id=1, name='Alan')
        sql.on_duplicate_key_update()
        self.assertEqual(str(sql), 'REPLACE INTO "user" ("id", "name") VALUES (1, \'Alan\')')
