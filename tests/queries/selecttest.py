
import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._queries.select
import sqlpuzzle.relations


class SelectTest(unittest.TestCase):
    def setUp(self):
        self.select = sqlpuzzle._queries.select.Select()


class BaseTest(SelectTest):
    def test_test(self):
        self.select.columns(1)
        self.assertEqual(str(self.select), 'SELECT 1')

    def test_simply(self):
        self.select.columns('id', 'name')
        self.select.from_('user')
        self.assertEqual(str(self.select), 'SELECT "id", "name" FROM "user"')

    def test_all_columns(self):
        self.select.from_('user')
        self.assertEqual(str(self.select), 'SELECT * FROM "user"')

    def test_all_columns_from_specific_table(self):
        self.select.columns('user.*').from_('user')
        self.assertEqual(str(self.select), 'SELECT "user".* FROM "user"')

    def test_order_by(self):
        self.select.from_('user')
        self.select.order_by('id')
        self.assertEqual(str(self.select), 'SELECT * FROM "user" ORDER BY "id"')

    def test_group_by(self):
        self.select.from_('user')
        self.select.group_by('id')
        self.assertEqual(str(self.select), 'SELECT * FROM "user" GROUP BY "id"')


class TableTest(SelectTest):
    def test_from(self):
        self.select.from_('table')
        self.assertEqual(str(self.select), 'SELECT * FROM "table"')

    def test_from_table(self):
        self.select.from_table('table')
        self.assertEqual(str(self.select), 'SELECT * FROM "table"')

    def test_from_table_with_alias(self):
        self.select.from_table('table', 'asTable')
        self.assertEqual(str(self.select), 'SELECT * FROM "table" AS "asTable"')

    def test_from_tables(self):
        self.select.from_tables('table', 'table2')
        self.assertEqual(str(self.select), 'SELECT * FROM "table", "table2"')

    def test_from_tables_with_alias(self):
        self.select.from_tables(('table', 'asTable'), 'table2')
        self.assertEqual(str(self.select), 'SELECT * FROM "table" AS "asTable", "table2"')


class JoinTest(SelectTest):
    def test_join(self):
        self.select.from_('user').join('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.select), 'SELECT * FROM "user" JOIN "country" ON "user"."country_id" = "country"."id"')

    def test_inner_join(self):
        self.select.from_('user').inner_join('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.select), 'SELECT * FROM "user" JOIN "country" ON "user"."country_id" = "country"."id"')

    def test_left_join(self):
        self.select.from_('user').left_join('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.select), 'SELECT * FROM "user" LEFT JOIN "country" ON "user"."country_id" = "country"."id"')

    def test_right_join(self):
        self.select.from_('user').right_join('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.select), 'SELECT * FROM "user" RIGHT JOIN "country" ON "user"."country_id" = "country"."id"')


class WhereTest(SelectTest):
    def test_where(self):
        self.select.from_('user')
        self.select.where(age=42)
        self.select.where('name', sqlpuzzle.relations.LIKE('Harry'))
        self.select.where({
            'sex': 'male',
        })
        self.select.where((
            ('enabled', 1),
        ))
        self.assertEqual(str(self.select), 'SELECT * FROM "user" WHERE "age" = 42 AND "name" LIKE \'Harry\' AND "sex" = \'male\' AND "enabled" = 1')


class HavingTest(SelectTest):
    def test_where(self):
        self.select.from_('user')
        self.select.having(age=42)
        self.select.having('name', sqlpuzzle.relations.LIKE('Harry'))
        self.select.having({
            'sex': 'male',
        })
        self.select.having((
            ('enabled', 1),
        ))
        self.assertEqual(str(self.select), 'SELECT * FROM "user" HAVING "age" = 42 AND "name" LIKE \'Harry\' AND "sex" = \'male\' AND "enabled" = 1')


class LimitTest(SelectTest):
    def test_limit(self):
        self.select.from_('user')
        self.select.limit(10)
        self.assertEqual(str(self.select), 'SELECT * FROM "user" LIMIT 10')

    def test_offset(self):
        self.select.from_('user')
        self.select.offset(40)
        self.assertEqual(str(self.select), 'SELECT * FROM "user" OFFSET 40')

    def test_limit_with_offset(self):
        self.select.from_('user')
        self.select.limit(10, 40)
        self.assertEqual(str(self.select), 'SELECT * FROM "user" LIMIT 10 OFFSET 40')

    def test_limit_offset(self):
        self.select.from_('user')
        self.select.limit(20)
        self.select.offset(30)
        self.assertEqual(str(self.select), 'SELECT * FROM "user" LIMIT 20 OFFSET 30')


class IntoOutfileTest(SelectTest):
    def setUp(self):
        self.select = sqlpuzzle._queries.select.Select()
        self.select.from_('table')
        self.select.into_outfile('/tmp/file')

    def test_into_outfile(self):
        self.assertEqual(str(self.select), 'SELECT * FROM "table" INTO OUTFILE \'/tmp/file\'')

    def test_fields_terminated_by(self):
        self.select.fields_terminated_by(',')
        self.assertEqual(str(self.select), 'SELECT * FROM "table" INTO OUTFILE \'/tmp/file\' FIELDS TERMINATED BY \',\'')

    def test_lines_terminated_by(self):
        self.select.lines_terminated_by('"')
        self.assertEqual(str(self.select), 'SELECT * FROM "table" INTO OUTFILE \'/tmp/file\' LINES TERMINATED BY \'"\'')

    def test_optionally_enclosed_by(self):
        self.select.optionally_enclosed_by('\n')
        self.assertEqual(str(self.select), 'SELECT * FROM "table" INTO OUTFILE \'/tmp/file\' OPTIONALLY ENCLOSED BY \'\\n\'')

    def test_all_in_one(self):
        self.select.fields_terminated_by(',')
        self.select.lines_terminated_by('"')
        self.select.optionally_enclosed_by('\n')
        self.assertEqual(str(self.select), 'SELECT * FROM "table" INTO OUTFILE \'/tmp/file\' FIELDS TERMINATED BY \',\' LINES TERMINATED BY \'"\' OPTIONALLY ENCLOSED BY \'\\n\'')


class SelectOptionsTest(SelectTest):
    def test_sql_cache(self):
        self.select.from_('table').sql_cache()
        self.assertEqual(str(self.select), 'SELECT SQL_CACHE * FROM "table"')

    def test_sql_cache_off(self):
        self.select.from_('table').sql_cache().sql_cache(False)
        self.assertEqual(str(self.select), 'SELECT * FROM "table"')

    def test_sql_no_cache(self):
        self.select.from_('table').sql_no_cache()
        self.assertEqual(str(self.select), 'SELECT SQL_NO_CACHE * FROM "table"')

    def test_sql_no_cache_off(self):
        self.select.from_('table').sql_no_cache().sql_no_cache(False)
        self.assertEqual(str(self.select), 'SELECT * FROM "table"')

    def test_all(self):
        self.select.from_('table').all()
        self.assertEqual(str(self.select), 'SELECT ALL * FROM "table"')

    def test_all_off(self):
        self.select.from_('table').all().all(False)
        self.assertEqual(str(self.select), 'SELECT * FROM "table"')

    def test_distinct(self):
        self.select.from_('table').distinct()
        self.assertEqual(str(self.select), 'SELECT DISTINCT * FROM "table"')

    def test_distinct_off(self):
        self.select.from_('table').distinct().distinct(False)
        self.assertEqual(str(self.select), 'SELECT * FROM "table"')

    def test_distinctrow(self):
        self.select.from_('table').distinctrow()
        self.assertEqual(str(self.select), 'SELECT DISTINCTROW * FROM "table"')

    def test_distinctrow_off(self):
        self.select.from_('table').distinctrow().distinctrow(False)
        self.assertEqual(str(self.select), 'SELECT * FROM "table"')

    def test_sql_small_result(self):
        self.select.from_('table').sql_small_result()
        self.assertEqual(str(self.select), 'SELECT SQL_SMALL_RESULT * FROM "table"')

    def test_sql_small_result_off(self):
        self.select.from_('table').sql_small_result().sql_small_result(False)
        self.assertEqual(str(self.select), 'SELECT * FROM "table"')

    def test_sql_big_result(self):
        self.select.from_('table').sql_big_result()
        self.assertEqual(str(self.select), 'SELECT SQL_BIG_RESULT * FROM "table"')

    def test_sql_big_result_off(self):
        self.select.from_('table').sql_big_result().sql_big_result(False)
        self.assertEqual(str(self.select), 'SELECT * FROM "table"')

    def test_sql_buffer_result(self):
        self.select.from_('table').sql_buffer_result()
        self.assertEqual(str(self.select), 'SELECT SQL_BUFFER_RESULT * FROM "table"')

    def test_sql_buffer_result_off(self):
        self.select.from_('table').sql_buffer_result().sql_buffer_result(False)
        self.assertEqual(str(self.select), 'SELECT * FROM "table"')

    def test_sql_calc_found_rows(self):
        self.select.from_('table').sql_calc_found_rows()
        self.assertEqual(str(self.select), 'SELECT SQL_CALC_FOUND_ROWS * FROM "table"')

    def test_sql_calc_found_rows_off(self):
        self.select.from_('table').sql_calc_found_rows().sql_calc_found_rows(False)
        self.assertEqual(str(self.select), 'SELECT * FROM "table"')

    def test_straight_join(self):
        self.select.from_('table').straight_join()
        self.assertEqual(str(self.select), 'SELECT STRAIGHT_JOIN * FROM "table"')

    def test_straight_join_off(self):
        self.select.from_('table').straight_join().straight_join(False)
        self.assertEqual(str(self.select), 'SELECT * FROM "table"')

    def test_high_priority(self):
        self.select.from_('table').high_priority()
        self.assertEqual(str(self.select), 'SELECT HIGH_PRIORITY * FROM "table"')

    def test_high_priority_off(self):
        self.select.from_('table').high_priority().high_priority(False)
        self.assertEqual(str(self.select), 'SELECT * FROM "table"')

    def test_more_options(self):
        self.select.from_('table').distinct().sql_calc_found_rows().sql_no_cache()
        self.assertEqual(str(self.select), 'SELECT SQL_CALC_FOUND_ROWS SQL_NO_CACHE DISTINCT * FROM "table"')

    def test_select_for_update(self):
        self.select.from_('table').for_update()
        self.assertEqual(str(self.select), 'SELECT * FROM "table" FOR UPDATE')


class UnionTest(SelectTest):
    def test_union(self):
        self.select.from_('table')
        self.assertEqual(str(self.select | self.select), 'SELECT * FROM "table" UNION SELECT * FROM "table"')

    def test_union_all(self):
        self.select.from_('table')
        self.assertEqual(str(self.select & self.select), 'SELECT * FROM "table" UNION ALL SELECT * FROM "table"')


class SubselectTest(SelectTest):
    def test_subselect_in_columns(self):
        subselect = sqlpuzzle._queries.select.Select('col').from_('tab')
        self.select.columns((subselect, 'c'))
        self.select.from_('tab')
        self.assertEqual(str(self.select), 'SELECT (SELECT "col" FROM "tab") AS "c" FROM "tab"')

    def test_subselect_in_columns_by_dictionary(self):
        subselect = sqlpuzzle._queries.select.Select('col').from_('tab')
        self.select.columns({subselect: 'c'})
        self.select.from_('tab')
        self.assertEqual(str(self.select), 'SELECT (SELECT "col" FROM "tab") AS "c" FROM "tab"')

    def test_subselect_in_tables(self):
        subselect = sqlpuzzle._queries.select.Select('col').from_('tab')
        self.select.from_((subselect, 't'))
        self.assertEqual(str(self.select), 'SELECT * FROM (SELECT "col" FROM "tab") AS "t"')

    def test_subselect_in_condition(self):
        subselect = sqlpuzzle._queries.select.Select('col').from_('tab')
        self.select.from_('tab')
        self.select.where(subselect, sqlpuzzle.relations.LE(42))
        self.assertEqual(str(self.select), 'SELECT * FROM "tab" WHERE (SELECT "col" FROM "tab") <= 42')

    def test_subselect_reference(self):
        subselect = sqlpuzzle._queries.select.Select('col').from_('t1').where('t1.a', '"t2".a')
        self.select.columns(subselect)
        self.select.from_('t2')
        self.assertEqual(str(self.select), 'SELECT (SELECT "col" FROM "t1" WHERE "t1"."a" = "t2"."a") FROM "t2"')


class CopyTest(SelectTest):
    def test_copy(self):
        self.select.from_('user').where(name='Alan')
        copy = self.select.copy()
        self.select.limit(10)
        self.assertEqual(str(copy), 'SELECT * FROM "user" WHERE "name" = \'Alan\'')
        self.assertEqual(str(self.select), 'SELECT * FROM "user" WHERE "name" = \'Alan\' LIMIT 10')

    def test_equals(self):
        self.select.from_('user').where(name='Alan')
        copy = self.select.copy()
        self.assertEqual(str(self.select), str(copy))

    def test_not_equals(self):
        self.select.from_('user').where(name='Alan')
        copy = self.select.copy()
        self.select.limit(10)
        self.assertFalse(self.select == copy)
