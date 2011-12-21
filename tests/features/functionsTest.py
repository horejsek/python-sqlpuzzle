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



testCases = (
    AvgTest,
    CountTest,
    MaxTest,
    MinTest,
    SumTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)
