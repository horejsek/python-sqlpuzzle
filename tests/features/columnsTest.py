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



class BaseTest(ColumnsTest):
    def testIsNotSet(self):
        self.assertEqual(self.columns.isSet(), False)
    
    def testIsSet(self):
        self.columns.columns('id')
        self.assertEqual(self.columns.isSet(), True)
    
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



class BackQuotesTest(ColumnsTest):
    def testColumnNameAsTableAndColumn(self):
        self.columns.columns('table.column')
        self.assertEqual(str(self.columns), '`table`.`column`')
    
    def testColumnNameAsTableAndColumnWithDotInName(self):
        self.columns.columns('table.`column.`')
        self.assertEqual(str(self.columns), '`table`.`column.`')



class GroupingTest(ColumnsTest):
    def testMoreSameColumnsPrintAsOne(self):
        self.columns.columns('col', 'col')
        self.assertEqual(str(self.columns), '`col`')
    
    def testMoreSameColumnsWithDiffAsPrintAsMore(self):
        self.columns.columns('col', ('col', 'col2'))
        self.assertEqual(str(self.columns), '`col`, `col` AS "col2"')



class ExceptionsTest(ColumnsTest):
    def testNameAsIntegerException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.columns.columns, 42)
    
    def testNameAsFloatException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.columns.columns, 42.1)
    
    def testNameAsBooleanException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.columns.columns, True)



testCases = (
    BaseTest,
    BackQuotesTest,
    GroupingTest,
    ExceptionsTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

