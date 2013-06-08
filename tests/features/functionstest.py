
import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._features.functions


class FunctionsTest(unittest.TestCase):
    pass


class AvgTest(FunctionsTest):
    def test_normal(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Avg('col')), 'AVG(`col`)')

    def test_distinct(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Avg('col', True)), 'AVG(DISTINCT `col`)')

    def test_distinct_by_method(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Avg('col').distinct()), 'AVG(DISTINCT `col`)')

    def test_distinct_by_method_with_param(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Avg('col').distinct(False)), 'AVG(`col`)')


class CountTest(FunctionsTest):
    def test_normal(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Count('col')), 'COUNT(`col`)')

    def test_count_with_star(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Count('*')), 'COUNT(*)')

    def test_count_without_param(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Count()), 'COUNT(*)')

    def test_distinct(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Count('col', True)), 'COUNT(DISTINCT `col`)')

    def test_distinct_by_method(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Count('col').distinct()), 'COUNT(DISTINCT `col`)')

    def test_distinct_by_method_with_param(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Count('col').distinct(False)), 'COUNT(`col`)')

    def test_distinct_more_exprs(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Count(('col1', 'col2')).distinct()), 'COUNT(DISTINCT `col1`, `col2`)')


class MaxTest(FunctionsTest):
    def test_normal(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Max('col')), 'MAX(`col`)')

    def test_distinct(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Max('col', True)), 'MAX(DISTINCT `col`)')

    def test_distinct_by_method(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Max('col').distinct()), 'MAX(DISTINCT `col`)')

    def test_distinct_by_method_with_param(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Max('col').distinct(False)), 'MAX(`col`)')


class MinTest(FunctionsTest):
    def test_normal(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Min('col')), 'MIN(`col`)')

    def test_distinct(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Min('col', True)), 'MIN(DISTINCT `col`)')

    def test_distinct_by_method(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Min('col').distinct()), 'MIN(DISTINCT `col`)')

    def test_distinct_by_method_with_param(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Min('col').distinct(False)), 'MIN(`col`)')


class SumTest(FunctionsTest):
    def test_normal(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Sum('col')), 'SUM(`col`)')

    def test_distinct(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Sum('col', True)), 'SUM(DISTINCT `col`)')

    def test_distinct_by_method(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Sum('col').distinct()), 'SUM(DISTINCT `col`)')

    def test_distinct_by_method_with_param(self):
        self.assertEqual(str(sqlpuzzle._features.functions.Sum('col').distinct(False)), 'SUM(`col`)')


class Concat(FunctionsTest):
    def test_normal(self):
        concat = sqlpuzzle._features.functions.Concat('col')
        self.assertEqual(str(concat), 'CONCAT(`col`)')

    def test_more_columns(self):
        concat = sqlpuzzle._features.functions.Concat('col', 'col2')
        self.assertEqual(str(concat), 'CONCAT(`col`, `col2`)')


class GroupConcat(FunctionsTest):
    def setUp(self):
        self.group_concat = sqlpuzzle._features.functions.GroupConcat('col')

    def test_normal(self):
        self.assertEqual(str(self.group_concat), 'GROUP_CONCAT(`col`)')

    def test_more_columns(self):
        group_concat = sqlpuzzle._features.functions.GroupConcat('col', 'col2')
        self.assertEqual(str(group_concat), 'GROUP_CONCAT(`col`, `col2`)')

    def test_with_order_by(self):
        self.group_concat.order_by({'name': 'desc'})
        self.assertEqual(str(self.group_concat), 'GROUP_CONCAT(`col` ORDER BY `name` DESC)')

    def test_with_separator(self):
        self.group_concat.separator('|||')
        self.assertEqual(str(self.group_concat), 'GROUP_CONCAT(`col` SEPARATOR "|||")')

    def test_with_order_by_and_separator(self):
        self.group_concat.order_by({'name': 'desc'}).separator('|||')
        self.assertEqual(str(self.group_concat), 'GROUP_CONCAT(`col` ORDER BY `name` DESC SEPARATOR "|||")')


class Convert(FunctionsTest):
    def setUp(self):
        self.convert = sqlpuzzle._features.functions.Convert('col')

    def test_signed(self):
        self.convert.to('signed')
        self.assertEqual(str(self.convert), 'CONVERT(`col`, SIGNED)')

    def test_char_with_length(self):
        self.convert.to('char(5)')
        self.assertEqual(str(self.convert), 'CONVERT(`col`, CHAR(5))')

    def test_decimal_with_precision(self):
        self.convert.to('decimal(2,5)')
        self.assertEqual(str(self.convert), 'CONVERT(`col`, DECIMAL(2,5))')

    def test_bad_type(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.convert.to, 'hcar')

    def test_bad_param_of_type(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.convert.to, 'char(a)')

    def test_invalid_type(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.convert.to, 'char(a')
