# -*- coding: utf-8 -*-

import unittest

import sqlpuzzle


class MySqlTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sqlpuzzle.configure('mysql')

    @classmethod
    def tearDownClass(cls):
        sqlpuzzle.configure('sql')

    def test_reference(self):
        sql = sqlpuzzle.select('id').from_('table')
        self.assertEqual(str(sql), 'SELECT `id` FROM `table`')

    def test_boolean(self):
        sql = sqlpuzzle.select_from('table').where({'flag': True})
        self.assertEqual(str(sql), 'SELECT * FROM `table` WHERE `flag` = 1')
