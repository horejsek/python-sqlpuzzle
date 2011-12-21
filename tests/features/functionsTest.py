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



class Concat(FunctionsTest):
    def testNormal(self):
        concat = sqlpuzzle._features.functions.Concat('col')
        self.assertEqual(str(concat), 'CONCAT(`col`)')

    def testMoreColumns(self):
        concat = sqlpuzzle._features.functions.Concat('col', 'col2')
        self.assertEqual(str(concat), 'CONCAT(`col`, `col2`)')



class GroupConcat(FunctionsTest):
    def setUp(self):
        self.groupConcat = sqlpuzzle._features.functions.GroupConcat('col')

    def testNormal(self):
        self.assertEqual(str(self.groupConcat), 'GROUP_CONCAT(`col`)')

    def testMoreColumns(self):
        groupConcat = sqlpuzzle._features.functions.GroupConcat('col', 'col2')
        self.assertEqual(str(groupConcat), 'GROUP_CONCAT(`col`, `col2`)')

    def testWithOrderBy(self):
        self.groupConcat.orderBy({'name': 'desc'})
        self.assertEqual(str(self.groupConcat), 'GROUP_CONCAT(`col` ORDER BY `name` DESC)')

    def testWithSeparator(self):
        self.groupConcat.separator('|||')
        self.assertEqual(str(self.groupConcat), 'GROUP_CONCAT(`col` SEPARATOR "|||")')

    def testWithOrderByAndSeparator(self):
        self.groupConcat.orderBy({'name': 'desc'}).separator('|||')
        self.assertEqual(str(self.groupConcat), 'GROUP_CONCAT(`col` ORDER BY `name` DESC SEPARATOR "|||")')



class Convert(FunctionsTest):
    def setUp(self):
        self.convert = sqlpuzzle._features.functions.Convert('col')

    def testSigned(self):
        self.convert.to('signed')
        self.assertEqual(str(self.convert), 'CONVERT(`col`, SIGNED)')

    def testCharWithLength(self):
        self.convert.to('char(5)')
        self.assertEqual(str(self.convert), 'CONVERT(`col`, CHAR(5))')

    def testDecimalWithPrecision(self):
        self.convert.to('decimal(2,5)')
        self.assertEqual(str(self.convert), 'CONVERT(`col`, DECIMAL(2,5))')

    def testBadType(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.convert.to, 'hcar')

    def testBadParamOfType(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.convert.to, 'char(a)')

    def testInvalidType(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.convert.to, 'char(a')



testCases = (
    AvgTest,
    CountTest,
    MaxTest,
    MinTest,
    SumTest,
    Concat,
    GroupConcat,
    Convert,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)
