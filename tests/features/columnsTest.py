# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.exceptions
import sqlPuzzle.features.columns


class ColumnsTest(unittest.TestCase):
    def setUp(self):
        self.columns = sqlPuzzle.features.columns.Columns()

    def tearDown(self):
        self.columns = sqlPuzzle.features.columns.Columns()
    
    def testOneColumn(self):
        self.columns.columns('id')
        self.assertEqual(str(self.columns), '`id`')
    
    def testMoreColumns(self):
        self.columns.columns('id', 'name')
        self.assertEqual(str(self.columns), '`id`, `name`')
    
    def testAllColumns(self):
        self.assertEqual(str(self.columns), '*')
    
    def testColumnAs(self):
        self.columns.columns(('id', 'ID'), 'name')
        self.assertEqual(str(self.columns), '`id` AS "ID", `name`')
    
    def testColumnNameAsTableAndColumn(self):
        self.columns.columns('table.column')
        self.assertEqual(str(self.columns), '`table`.`column`')
    
    def testColumnNameAsTableAndColumnWithDotInName(self):
        self.columns.columns('table.`column.`')
        self.assertEqual(str(self.columns), '`table`.`column.`')
    
    def testMoreSameColumnsPrintAsOne(self):
        self.columns.columns('col', 'col')
        self.assertEqual(str(self.columns), '`col`')
    
    def testMoreSameColumnsWithDiffAsPrintAsMore(self):
        self.columns.columns('col', ('col', 'col2'))
        self.assertEqual(str(self.columns), '`col`, `col` AS "col2"')
    
    def testNameAsIntegerException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.columns.columns, 42)
    
    def testNameAsFloatException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.columns.columns, 42.1)
    
    def testNameAsBooleanException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.columns.columns, True)
    
    def testIsSet(self):
        self.assertEqual(self.columns.isSet(), False)
        self.columns.columns('id')
        self.assertEqual(self.columns.isSet(), True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LimitTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

