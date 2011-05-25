# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.columns


class ColumnsTest(unittest.TestCase):
    def setUp(self):
        self.columns = sqlPuzzle.columns.Columns()

    def tearDown(self):
        self.columns = sqlPuzzle.columns.Columns()
    
    def testColumnsOne(self):
        self.columns.columns('id')
        self.assertEqual(str(self.columns), '`id`')
    
    def testColumnsMore(self):
        self.columns.columns('id', 'name')
        self.assertEqual(str(self.columns), '`id`, `name`')
    
    def testColumnsAll(self):
        self.assertEqual(str(self.columns), '*')
    
    def testColumnsAs(self):
        self.columns.columns(('id', 'ID'), 'name')
        self.assertEqual(str(self.columns), '`id` AS "ID", `name`')
    
    def testIsSet(self):
        self.assertEqual(self.columns.isSet(), False)
        self.columns.columns('id')
        self.assertEqual(self.columns.isSet(), True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LimitTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

