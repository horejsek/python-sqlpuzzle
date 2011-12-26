# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import unittest

import sqlpuzzle._features.groupBy


class GroupByTest(unittest.TestCase):
    def setUp(self):
        self.groupBy = sqlpuzzle._features.groupBy.GroupBy()



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

    def testByDictionary(self):
        self.groupBy.groupBy({'id': 'ASC', 'name': 'DESC'})
        self.assertEqual(str(self.groupBy), 'GROUP BY `id`, `name` DESC')

    def testByKwds(self):
        self.groupBy.groupBy(id='ASC', name='DESC')
        self.assertEqual(str(self.groupBy), 'GROUP BY `id`, `name` DESC')



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



class CopyTest(GroupByTest):
    def testCopy(self):
        self.groupBy.groupBy('id', 'name')
        copy = self.groupBy.copy()
        self.groupBy.groupBy('address')
        self.assertEqual(str(copy), 'GROUP BY `id`, `name`')
        self.assertEqual(str(self.groupBy), 'GROUP BY `id`, `name`, `address`')

    def testEquals(self):
        self.groupBy.groupBy('id', 'name')
        copy = self.groupBy.copy()
        self.assertTrue(self.groupBy == copy)

    def testNotEquals(self):
        self.groupBy.groupBy('id', 'name')
        copy = self.groupBy.copy()
        self.groupBy.groupBy('address')
        self.assertFalse(self.groupBy == copy)



class ExceptionsTest(GroupByTest):
    def testNameAsFloatException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.groupBy.groupBy, 42.1)

    def testNameAsBooleanException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.groupBy.groupBy, True)

    def testNotAscOrDescException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.groupBy.groupBy, ('col', 'AAA'))



testCases = (
    BaseTest,
    BackQuotesTest,
    GroupingTest,
    CopyTest,
    ExceptionsTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)
