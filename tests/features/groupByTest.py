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



class BaseTest(GroupByTest):
    def testIsNotSet(self):
        self.assertEqual(self.groupBy.isSet(), False)
    
    def testIsSet(self):
        self.groupBy.groupBy('id')
        self.assertEqual(self.groupBy.isSet(), True)
    
    def testSimply(self):
        self.groupBy.groupBy('id')
        self.assertEqual(str(self.groupBy), 'GROUP BY `id`')
    
    def testMoreColumns(self):
        self.groupBy.groupBy('id', ['name', 'desc'])
        self.assertEqual(str(self.groupBy), 'GROUP BY `id`, `name` DESC')
    
    def testASC(self):
        self.groupBy.groupBy(['name', 'asc'])
        self.assertEqual(str(self.groupBy), 'GROUP BY `name`')
    
    def testDESC(self):
        self.groupBy.groupBy(['name', 'desc'])
        self.assertEqual(str(self.groupBy), 'GROUP BY `name` DESC')
    
    def testOrderByNumber(self):
        self.groupBy.groupBy(1)
        self.assertEqual(str(self.groupBy), 'GROUP BY 1')



class BackQuotesTest(GroupByTest):
    def testColumnNameAsTableAndColumn(self):
        self.groupBy.groupBy('table.column')
        self.assertEqual(str(self.groupBy), 'GROUP BY `table`.`column`')
    
    def testColumnNameAsTableAndColumnWithDotInName(self):
        self.groupBy.groupBy('table.`column.`')
        self.assertEqual(str(self.groupBy), 'GROUP BY `table`.`column.`')



class GroupingTest(GroupByTest):
    def testMoreSameColumnsPrintAsOne(self):
        self.groupBy.groupBy('col', 'col')
        self.assertEqual(str(self.groupBy), 'GROUP BY `col`')
    
    def testMoreSameColumnsWithDiffAscPrintAsOne(self):
        self.groupBy.groupBy('col', ('col', 'DESC'))
        self.assertEqual(str(self.groupBy), 'GROUP BY `col` DESC')



class ExceptionsTest(GroupByTest):
    def testNameAsFloatException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.groupBy.groupBy, 42.1)
    
    def testNameAsBooleanException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.groupBy.groupBy, True)
    
    def testNotAscOrDescException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.groupBy.groupBy, ('col', 'AAA'))



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

