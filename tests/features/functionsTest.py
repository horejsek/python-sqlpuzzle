# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._features.functions


class FunctionsTest(unittest.TestCase):
    pass



class AvgTest(FunctionsTest):
    def testNormal(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Avg('col')), 'AVG(`col`)')

    def testDistinct(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Avg('col', True)), 'AVG(DISTINCT `col`)')

    def testDistinctByMethod(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Avg('col').distinct()), 'AVG(DISTINCT `col`)')

    def testDistinctByMethodWithParam(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Avg('col').distinct(False)), 'AVG(`col`)')



class CountTest(FunctionsTest):
    def testNormal(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Count('col')), 'COUNT(`col`)')

    def testDistinct(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Count('col', True)), 'COUNT(DISTINCT `col`)')

    def testDistinctByMethod(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Count('col').distinct()), 'COUNT(DISTINCT `col`)')

    def testDistinctByMethodWithParam(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Count('col').distinct(False)), 'COUNT(`col`)')

    def testCountWithStar(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Count('*')), 'COUNT(*)')

    def testCountWithoutParam(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Count()), 'COUNT(*)')



class MaxTest(FunctionsTest):
    def testNormal(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Max('col')), 'MAX(`col`)')

    def testDistinct(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Max('col', True)), 'MAX(DISTINCT `col`)')

    def testDistinctByMethod(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Max('col').distinct()), 'MAX(DISTINCT `col`)')

    def testDistinctByMethodWithParam(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Max('col').distinct(False)), 'MAX(`col`)')



class MinTest(FunctionsTest):
    def testNormal(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Min('col')), 'MIN(`col`)')

    def testDistinct(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Min('col', True)), 'MIN(DISTINCT `col`)')

    def testDistinctByMethod(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Min('col').distinct()), 'MIN(DISTINCT `col`)')

    def testDistinctByMethodWithParam(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Min('col').distinct(False)), 'MIN(`col`)')



class SumTest(FunctionsTest):
    def testNormal(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Sum('col')), 'SUM(`col`)')

    def testDistinct(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Sum('col', True)), 'SUM(DISTINCT `col`)')

    def testDistinctByMethod(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Sum('col').distinct()), 'SUM(DISTINCT `col`)')

    def testDistinctByMethodWithParam(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Sum('col').distinct(False)), 'SUM(`col`)')



class GroupConcat(FunctionsTest):
    def setUp(self):
        self.groupConcat = sqlpuzzle._features.functions.GroupConcat('col')

    def testNormal(self):
        self.assertEqual(str(self.groupConcat), 'GROUP_CONCAT(`col`)')

    def testWithOrderBy(self):
        self.groupConcat.orderBy({'name': 'desc'})
        self.assertEqual(str(self.groupConcat), 'GROUP_CONCAT(`col` ORDER BY `name` DESC)')

    def testWithSeparator(self):
        self.groupConcat.separator('|||')
        self.assertEqual(str(self.groupConcat), 'GROUP_CONCAT(`col` SEPARATOR "|||")')

    def testWithOrderByAndSeparator(self):
        self.groupConcat.orderBy({'name': 'desc'}).separator('|||')
        self.assertEqual(str(self.groupConcat), 'GROUP_CONCAT(`col` ORDER BY `name` DESC SEPARATOR "|||")')



testCases = (
    AvgTest,
    CountTest,
    MaxTest,
    MinTest,
    SumTest,
    GroupConcat,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)
