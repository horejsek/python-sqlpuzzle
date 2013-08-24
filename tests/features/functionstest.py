# -*- coding: utf-8 -*-

import unittest

import sqlpuzzle
from sqlpuzzle._queryparts import Avg, Concat, Convert, Count, GroupConcat, Max, Min, Sum


class FunctionsTest(unittest.TestCase):
    pass


class AvgTest(FunctionsTest):
    def test_normal(self):
        self.assertEqual(str(Avg('col')), 'AVG(`col`)')

    def test_distinct(self):
        self.assertEqual(str(Avg('col', True)), 'AVG(DISTINCT `col`)')

    def test_distinct_by_method(self):
        self.assertEqual(str(Avg('col').distinct()), 'AVG(DISTINCT `col`)')

    def test_distinct_by_method_with_param(self):
        self.assertEqual(str(Avg('col').distinct(False)), 'AVG(`col`)')


class CountTest(FunctionsTest):
    def test_normal(self):
        self.assertEqual(str(Count('col')), 'COUNT(`col`)')

    def test_count_with_star(self):
        self.assertEqual(str(Count('*')), 'COUNT(*)')

    def test_count_without_param(self):
        self.assertEqual(str(Count()), 'COUNT(*)')

    def test_distinct(self):
        self.assertEqual(str(Count('col', True)), 'COUNT(DISTINCT `col`)')

    def test_distinct_by_method(self):
        self.assertEqual(str(Count('col').distinct()), 'COUNT(DISTINCT `col`)')

    def test_distinct_by_method_with_param(self):
        self.assertEqual(str(Count('col').distinct(False)), 'COUNT(`col`)')

    def test_distinct_more_exprs(self):
        self.assertEqual(str(Count(('col1', 'col2')).distinct()), 'COUNT(DISTINCT `col1`, `col2`)')


class MaxTest(FunctionsTest):
    def test_normal(self):
        self.assertEqual(str(Max('col')), 'MAX(`col`)')

    def test_distinct(self):
        self.assertEqual(str(Max('col', True)), 'MAX(DISTINCT `col`)')

    def test_distinct_by_method(self):
        self.assertEqual(str(Max('col').distinct()), 'MAX(DISTINCT `col`)')

    def test_distinct_by_method_with_param(self):
        self.assertEqual(str(Max('col').distinct(False)), 'MAX(`col`)')


class MinTest(FunctionsTest):
    def test_normal(self):
        self.assertEqual(str(Min('col')), 'MIN(`col`)')

    def test_distinct(self):
        self.assertEqual(str(Min('col', True)), 'MIN(DISTINCT `col`)')

    def test_distinct_by_method(self):
        self.assertEqual(str(Min('col').distinct()), 'MIN(DISTINCT `col`)')

    def test_distinct_by_method_with_param(self):
        self.assertEqual(str(Min('col').distinct(False)), 'MIN(`col`)')


class SumTest(FunctionsTest):
    def test_normal(self):
        self.assertEqual(str(Sum('col')), 'SUM(`col`)')

    def test_distinct(self):
        self.assertEqual(str(Sum('col', True)), 'SUM(DISTINCT `col`)')

    def test_distinct_by_method(self):
        self.assertEqual(str(Sum('col').distinct()), 'SUM(DISTINCT `col`)')

    def test_distinct_by_method_with_param(self):
        self.assertEqual(str(Sum('col').distinct(False)), 'SUM(`col`)')


class ConcatTest(FunctionsTest):
    def test_normal(self):
        concat = Concat('col')
        self.assertEqual(str(concat), 'CONCAT(`col`)')

    def test_more_columns(self):
        concat = Concat('col', 'col2')
        self.assertEqual(str(concat), 'CONCAT(`col`, `col2`)')


class GroupConcatTest(FunctionsTest):
    def setUp(self):
        self.group_concat = GroupConcat('col')

    def test_normal(self):
        self.assertEqual(str(self.group_concat), 'GROUP_CONCAT(`col`)')

    def test_more_columns(self):
        group_concat = GroupConcat('col', 'col2')
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


class ConvertTest(FunctionsTest):
    def setUp(self):
        self.convert = Convert('col')

    def test_signed(self):
        self.convert.to('signed')
        self.assertEqual(str(self.convert), 'CONVERT(`col`, SIGNED)')

    def test_char_with_length(self):
        self.convert.to('char(5)')
        self.assertEqual(str(self.convert), 'CONVERT(`col`, CHAR(5))')

    def test_decimal_with_precision(self):
        self.convert.to('decimal(2,5)')
        self.assertEqual(str(self.convert), 'CONVERT(`col`, DECIMAL(2,5))')
