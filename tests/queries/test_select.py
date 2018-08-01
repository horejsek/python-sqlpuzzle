# pylint: disable=invalid-name

from unittest import mock

import sqlpuzzle.exceptions
from sqlpuzzle._backends.sql import SqlBackend
import sqlpuzzle.relations


def test_base(select):
    select.columns(1)
    assert str(select) == 'SELECT 1'


def test_simply(select):
    select.columns('id', 'name')
    select.from_('user')
    assert str(select) == 'SELECT "id", "name" FROM "user"'


def test_all_columns(select):
    select.from_('user')
    assert str(select) == 'SELECT * FROM "user"'


def test_all_columns_from_specific_table(select):
    select.columns('user.*').from_('user')
    assert str(select) == 'SELECT "user".* FROM "user"'


def test_order_by(select):
    select.from_('user')
    select.order_by('id')
    assert str(select) == 'SELECT * FROM "user" ORDER BY "id"'


def test_group_by(select):
    select.from_('user')
    select.group_by('id')
    assert str(select) == 'SELECT * FROM "user" GROUP BY "id"'


def test_str(select):
    select.from_('user')
    select.where(name='ščřž')
    assert str(select) == 'SELECT * FROM "user" WHERE "name" = \'ščřž\''


def test_has_not_where(select):
    assert not select.has('where')


def test_has_where(select):
    select.where(id=1)
    assert select.has('where')
    assert select.has('where', 'id')


def test_has_not_distinct(select):
    assert not select.has('distinct')
    select.distinctrow()
    assert not select.has('distinct')


def test_has_distinct(select):
    select.distinct()
    assert select.has('distinct')


def test_has_select_for_update(select):
    select.for_update()
    assert select.has('select_for_update')


def test_from(select):
    select.from_('table')
    assert str(select) == 'SELECT * FROM "table"'


def test_from_table(select):
    select.from_table('table')
    assert str(select) == 'SELECT * FROM "table"'


def test_from_table_with_alias(select):
    select.from_table('table', 'asTable')
    assert str(select) == 'SELECT * FROM "table" AS "asTable"'


def test_from_tables(select):
    select.from_tables('table', 'table2')
    assert str(select) == 'SELECT * FROM "table", "table2"'


def test_from_tables_with_alias(select):
    select.from_tables(('table', 'asTable'), 'table2')
    assert str(select) == 'SELECT * FROM "table" AS "asTable", "table2"'


def test_join(select):
    select.from_('user').join('country').on('user.country_id', 'country.id')
    assert str(select) == 'SELECT * FROM "user" JOIN "country" ON "user"."country_id" = "country"."id"'


def test_inner_join(select):
    select.from_('user').inner_join('country').on('user.country_id', 'country.id')
    assert str(select) == 'SELECT * FROM "user" JOIN "country" ON "user"."country_id" = "country"."id"'


def test_left_join(select):
    select.from_('user').left_join('country').on('user.country_id', 'country.id')
    assert str(select) == 'SELECT * FROM "user" LEFT JOIN "country" ON "user"."country_id" = "country"."id"'


def test_right_join(select):
    select.from_('user').right_join('country').on('user.country_id', 'country.id')
    assert str(select) == 'SELECT * FROM "user" RIGHT JOIN "country" ON "user"."country_id" = "country"."id"'


def test_full_join(select):
    with mock.patch.object(SqlBackend, 'supports_full_join', True):
        select.from_('user').full_join('country').on('user.country_id', 'country.id')
        assert str(select) == 'SELECT * FROM "user" FULL JOIN "country" ON "user"."country_id" = "country"."id"'


def test_where(select):
    select.from_('user')
    select.where(age=42)
    select.where('name', sqlpuzzle.relations.LIKE('Harry'))
    select.where({
        'sex': 'male',
    })
    select.where((
        ('enabled', 1),
    ))
    assert str(select) == (
        'SELECT * FROM "user" WHERE "age" = 42 AND "name" LIKE \'Harry\' AND "sex" = \'male\' AND "enabled" = 1'
    )


def test_having(select):
    select.from_('user')
    select.having(age=42)
    select.having('name', sqlpuzzle.relations.LIKE('Harry'))
    select.having({
        'sex': 'male',
    })
    select.having((
        ('enabled', 1),
    ))
    assert str(select) == (
        'SELECT * FROM "user" HAVING "age" = 42 AND "name" LIKE \'Harry\' AND "sex" = \'male\' AND "enabled" = 1'
    )


def test_limit(select):
    select.from_('user')
    select.limit(10)
    assert str(select) == 'SELECT * FROM "user" LIMIT 10'


def test_offset(select):
    select.from_('user')
    select.offset(40)
    assert str(select) == 'SELECT * FROM "user" OFFSET 40'


def test_limit_with_offset(select):
    select.from_('user')
    select.limit(10, 40)
    assert str(select) == 'SELECT * FROM "user" LIMIT 10 OFFSET 40'


def test_limit_offset(select):
    select.from_('user')
    select.limit(20)
    select.offset(30)
    assert str(select) == 'SELECT * FROM "user" LIMIT 20 OFFSET 30'


def test_into_outfile(select):
    select.from_('table').into_outfile('/tmp/file')
    assert str(select) == 'SELECT * FROM "table" INTO OUTFILE \'/tmp/file\''


def test_fields_terminated_by(select):
    select.from_('table').into_outfile('/tmp/file')
    select.fields_terminated_by(',')
    assert str(select) == 'SELECT * FROM "table" INTO OUTFILE \'/tmp/file\' FIELDS TERMINATED BY \',\''


def test_lines_terminated_by(select):
    select.from_('table').into_outfile('/tmp/file')
    select.lines_terminated_by('"')
    assert str(select) == 'SELECT * FROM "table" INTO OUTFILE \'/tmp/file\' LINES TERMINATED BY \'"\''


def test_optionally_enclosed_by(select):
    select.from_('table').into_outfile('/tmp/file')
    select.optionally_enclosed_by('\n')
    assert str(select) == 'SELECT * FROM "table" INTO OUTFILE \'/tmp/file\' OPTIONALLY ENCLOSED BY \'\\n\''


def test_all_in_one(select):
    select.from_('table').into_outfile('/tmp/file')
    select.fields_terminated_by(',')
    select.lines_terminated_by('"')
    select.optionally_enclosed_by('\n')
    assert str(select) == (
        'SELECT * FROM "table" INTO OUTFILE \'/tmp/file\''
        ' FIELDS TERMINATED BY \',\' LINES TERMINATED BY \'"\' OPTIONALLY ENCLOSED BY \'\\n\''
    )


def test_sql_cache(select):
    select.from_('table').sql_cache()
    assert str(select) == 'SELECT SQL_CACHE * FROM "table"'


def test_sql_cache_off(select):
    select.from_('table').sql_cache().sql_cache(False)
    assert str(select) == 'SELECT * FROM "table"'


def test_sql_no_cache(select):
    select.from_('table').sql_no_cache()
    assert str(select) == 'SELECT SQL_NO_CACHE * FROM "table"'


def test_sql_no_cache_off(select):
    select.from_('table').sql_no_cache().sql_no_cache(False)
    assert str(select) == 'SELECT * FROM "table"'


def test_all(select):
    select.from_('table').all()
    assert str(select) == 'SELECT ALL * FROM "table"'


def test_all_off(select):
    select.from_('table').all().all(False)
    assert str(select) == 'SELECT * FROM "table"'


def test_distinct(select):
    select.from_('table').distinct()
    assert str(select) == 'SELECT DISTINCT * FROM "table"'


def test_distinct_off(select):
    select.from_('table').distinct().distinct(False)
    assert str(select) == 'SELECT * FROM "table"'


def test_distinctrow(select):
    select.from_('table').distinctrow()
    assert str(select) == 'SELECT DISTINCTROW * FROM "table"'


def test_distinctrow_off(select):
    select.from_('table').distinctrow().distinctrow(False)
    assert str(select) == 'SELECT * FROM "table"'


def test_sql_small_result(select):
    select.from_('table').sql_small_result()
    assert str(select) == 'SELECT SQL_SMALL_RESULT * FROM "table"'


def test_sql_small_result_off(select):
    select.from_('table').sql_small_result().sql_small_result(False)
    assert str(select) == 'SELECT * FROM "table"'


def test_sql_big_result(select):
    select.from_('table').sql_big_result()
    assert str(select) == 'SELECT SQL_BIG_RESULT * FROM "table"'


def test_sql_big_result_off(select):
    select.from_('table').sql_big_result().sql_big_result(False)
    assert str(select) == 'SELECT * FROM "table"'


def test_sql_buffer_result(select):
    select.from_('table').sql_buffer_result()
    assert str(select) == 'SELECT SQL_BUFFER_RESULT * FROM "table"'


def test_sql_buffer_result_off(select):
    select.from_('table').sql_buffer_result().sql_buffer_result(False)
    assert str(select) == 'SELECT * FROM "table"'


def test_sql_calc_found_rows(select):
    select.from_('table').sql_calc_found_rows()
    assert str(select) == 'SELECT SQL_CALC_FOUND_ROWS * FROM "table"'


def test_sql_calc_found_rows_off(select):
    select.from_('table').sql_calc_found_rows().sql_calc_found_rows(False)
    assert str(select) == 'SELECT * FROM "table"'


def test_straight_join(select):
    select.from_('table').straight_join()
    assert str(select) == 'SELECT STRAIGHT_JOIN * FROM "table"'


def test_straight_join_off(select):
    select.from_('table').straight_join().straight_join(False)
    assert str(select) == 'SELECT * FROM "table"'


def test_high_priority(select):
    select.from_('table').high_priority()
    assert str(select) == 'SELECT HIGH_PRIORITY * FROM "table"'


def test_high_priority_off(select):
    select.from_('table').high_priority().high_priority(False)
    assert str(select) == 'SELECT * FROM "table"'


def test_more_options(select):
    select.from_('table').distinct().sql_calc_found_rows().sql_no_cache()
    assert str(select) == 'SELECT DISTINCT SQL_CALC_FOUND_ROWS SQL_NO_CACHE * FROM "table"'


def test_select_for_update(select):
    select.from_('table').for_update()
    assert str(select) == 'SELECT * FROM "table" FOR UPDATE'


def test_union(select):
    select.from_('table')
    assert str(select | select) == 'SELECT * FROM "table" UNION SELECT * FROM "table"'


def test_union_all(select):
    select.from_('table')
    assert str(select & select) == 'SELECT * FROM "table" UNION ALL SELECT * FROM "table"'


def test_subselect_in_columns(select):
    subselect = sqlpuzzle._queries.select.Select('col').from_('tab')
    select.columns((subselect, 'c'))
    select.from_('tab')
    assert str(select) == 'SELECT (SELECT "col" FROM "tab") AS "c" FROM "tab"'


def test_subselect_in_columns_by_dictionary(select):
    subselect = sqlpuzzle._queries.select.Select('col').from_('tab')
    select.columns({subselect: 'c'})
    select.from_('tab')
    assert str(select) == 'SELECT (SELECT "col" FROM "tab") AS "c" FROM "tab"'


def test_subselect_in_tables(select):
    subselect = sqlpuzzle._queries.select.Select('col').from_('tab')
    select.from_((subselect, 't'))
    assert str(select) == 'SELECT * FROM (SELECT "col" FROM "tab") AS "t"'


def test_subselect_in_condition(select):
    subselect = sqlpuzzle._queries.select.Select('col').from_('tab')
    select.from_('tab')
    select.where(subselect, sqlpuzzle.relations.LE(42))
    assert str(select) == 'SELECT * FROM "tab" WHERE (SELECT "col" FROM "tab") <= 42'


def test_subselect_reference(select):
    subselect = sqlpuzzle._queries.select.Select('col').from_('t1').where('t1.a', '"t2".a')
    select.columns(subselect)
    select.from_('t2')
    assert str(select) == 'SELECT (SELECT "col" FROM "t1" WHERE "t1"."a" = "t2"."a") FROM "t2"'


def test_copy(select):
    select.from_('user').where(name='Alan')
    copy = select.copy()
    select.limit(10)
    assert str(copy) == 'SELECT * FROM "user" WHERE "name" = \'Alan\''
    assert str(select) == 'SELECT * FROM "user" WHERE "name" = \'Alan\' LIMIT 10'


def test_equals(select):
    select.from_('user').where(name='Alan')
    copy = select.copy()
    assert str(select) == str(copy)


def test_not_equals(select):
    select.from_('user').where(name='Alan')
    copy = select.copy()
    select.limit(10)
    assert not select == copy
