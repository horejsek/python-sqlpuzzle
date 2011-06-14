# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.features.groupBy


class GroupByTest(unittest.TestCase):
    def setUp(self):
        self.groupBy = sqlPuzzle.features.groupBy.GroupBy()

    def tearDown(self):
        self.groupBy = sqlPuzzle.features.groupBy.GroupBy()
    
    def testSimply(self):
        self.groupBy.groupBy('id')
        self.assertEqual(str(self.groupBy), 'GROUP BY `id`')
    
    def testASC(self):
        self.groupBy.groupBy(['name', 'asc'])
        self.assertEqual(str(self.groupBy), 'GROUP BY `name`')
    
    def testDESC(self):
        self.groupBy.groupBy(['name', 'desc'])
        self.assertEqual(str(self.groupBy), 'GROUP BY `name` DESC')
    
    def testMore(self):
        self.groupBy.groupBy('id', ['name', 'desc'])
        self.assertEqual(str(self.groupBy), 'GROUP BY `id`, `name` DESC')
    
    def testColumnNameAsTableAndColumn(self):
        self.groupBy.groupBy('table.column')
        self.assertEqual(str(self.groupBy), 'GROUP BY `table`.`column`')
    
    def testColumnNameAsTableAndColumnWithDotInName(self):
        self.groupBy.groupBy('table.`column.`')
        self.assertEqual(str(self.groupBy), 'GROUP BY `table`.`column.`')
    
    def testMoreSameColumnsPrintAsOne(self):
        self.groupBy.groupBy('col', 'col')
        self.assertEqual(str(self.groupBy), 'GROUP BY `col`')
    
    def testMoreSameColumnsWithDiffAscPrintAsOne(self):
        self.groupBy.groupBy('col', ('col', 'DESC'))
        self.assertEqual(str(self.groupBy), 'GROUP BY `col` DESC')
    
    def testNameAsIntegerException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.groupBy.groupBy, 42)
    
    def testNameAsFloatException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.groupBy.groupBy, 42.1)
    
    def testNameAsBooleanException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.groupBy.groupBy, True)
    
    def testNotAscOrDescException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.groupBy.groupBy, ('col', 'AAA'))
    
    def testIsSet(self):
        self.assertEqual(self.groupBy.isSet(), False)
        self.groupBy.groupBy('id')
        self.assertEqual(self.groupBy.isSet(), True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GroupByTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

