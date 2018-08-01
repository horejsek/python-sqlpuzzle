# pylint: disable=invalid-name

from sqlpuzzle._queryparts import Avg, Concat, Convert, Count, GroupConcat, Max, Min, Sum


class TestAvg:
    def test_normal(self):
        assert str(Avg('col')) == 'AVG("col")'

    def test_distinct(self):
        assert str(Avg('col', True)) == 'AVG(DISTINCT "col")'

    def test_distinct_by_method(self):
        assert str(Avg('col').distinct()) == 'AVG(DISTINCT "col")'

    def test_distinct_by_method_with_param(self):
        assert str(Avg('col').distinct(False)) == 'AVG("col")'


class TestCount:
    def test_normal(self):
        assert str(Count('col')) == 'COUNT("col")'

    def test_count_with_star(self):
        assert str(Count('*')) == 'COUNT(*)'

    def test_count_without_param(self):
        assert str(Count()) == 'COUNT(*)'

    def test_distinct(self):
        assert str(Count('col', True)) == 'COUNT(DISTINCT "col")'

    def test_distinct_by_method(self):
        assert str(Count('col').distinct()) == 'COUNT(DISTINCT "col")'

    def test_distinct_by_method_with_param(self):
        assert str(Count('col').distinct(False)) == 'COUNT("col")'

    def test_distinct_more_exprs(self):
        assert str(Count(('col1', 'col2')).distinct()) == 'COUNT(DISTINCT "col1", "col2")'


class TestMax:
    def test_normal(self):
        assert str(Max('col')) == 'MAX("col")'

    def test_distinct(self):
        assert str(Max('col', True)) == 'MAX(DISTINCT "col")'

    def test_distinct_by_method(self):
        assert str(Max('col').distinct()) == 'MAX(DISTINCT "col")'

    def test_distinct_by_method_with_param(self):
        assert str(Max('col').distinct(False)) == 'MAX("col")'


class TestMin:
    def test_normal(self):
        assert str(Min('col')) == 'MIN("col")'

    def test_distinct(self):
        assert str(Min('col', True)) == 'MIN(DISTINCT "col")'

    def test_distinct_by_method(self):
        assert str(Min('col').distinct()) == 'MIN(DISTINCT "col")'

    def test_distinct_by_method_with_param(self):
        assert str(Min('col').distinct(False)) == 'MIN("col")'


class TestSum:
    def test_normal(self):
        assert str(Sum('col')) == 'SUM("col")'

    def test_distinct(self):
        assert str(Sum('col', True)) == 'SUM(DISTINCT "col")'

    def test_distinct_by_method(self):
        assert str(Sum('col').distinct()) == 'SUM(DISTINCT "col")'

    def test_distinct_by_method_with_param(self):
        assert str(Sum('col').distinct(False)) == 'SUM("col")'


class TestConcat:
    def test_normal(self):
        concat = Concat('col')
        assert str(concat) == 'CONCAT("col")'

    def test_more_columns(self):
        concat = Concat('col', 'col2')
        assert str(concat) == 'CONCAT("col", "col2")'


class TestGroupConcat:
    def test_normal(self):
        group_concat = GroupConcat('col')
        assert str(group_concat) == 'GROUP_CONCAT("col")'

    def test_more_columns(self):
        group_concat = GroupConcat('col', 'col2')
        assert str(group_concat) == 'GROUP_CONCAT("col", "col2")'

    def test_with_order_by(self):
        group_concat = GroupConcat('col')
        group_concat.order_by({'name': 'desc'})
        assert str(group_concat) == 'GROUP_CONCAT("col" ORDER BY "name" DESC)'

    def test_with_separator(self):
        group_concat = GroupConcat('col')
        group_concat.separator('|||')
        assert str(group_concat) == 'GROUP_CONCAT("col" SEPARATOR \'|||\')'

    def test_with_order_by_and_separator(self):
        group_concat = GroupConcat('col')
        group_concat.order_by({'name': 'desc'}).separator('|||')
        assert str(group_concat) == 'GROUP_CONCAT("col" ORDER BY "name" DESC SEPARATOR \'|||\')'


class TestConvert:
    def test_signed(self):
        convert = Convert('col')
        convert.to('signed')
        assert str(convert) == 'CONVERT("col", SIGNED)'

    def test_char_with_length(self):
        convert = Convert('col')
        convert.to('char(5)')
        assert str(convert) == 'CONVERT("col", CHAR(5))'

    def test_decimal_with_precision(self):
        convert = Convert('col')
        convert.to('decimal(2,5)')
        assert str(convert) == 'CONVERT("col", DECIMAL(2,5))'
