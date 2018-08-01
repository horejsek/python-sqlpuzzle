# pylint: disable=redefined-outer-name,invalid-name

from unittest import mock

import pytest

import sqlpuzzle
from sqlpuzzle import Q
from sqlpuzzle.exceptions import InvalidQueryException
from sqlpuzzle._backends.sql import SqlBackend
from sqlpuzzle._queryparts import Tables


@pytest.fixture
def tables():
    return Tables()


def test_is_not_set(tables):
    assert not tables.is_set


def test_is_set(tables):
    tables.set('table')
    assert tables.is_set


def test_is_simple(tables):
    tables.set('table')
    assert tables.is_simple()


def test_is_not_simple(tables):
    tables.set('table')
    tables.join('table2').on('id', 'id2')
    assert not tables.is_simple()


def test_simple(tables):
    tables.set('table')
    assert str(tables) == '"table"'


def test_simple_as(tables):
    tables.set(('table', 't1'))
    assert str(tables) == '"table" AS "t1"'


def test_more_tables(tables):
    tables.set('user', 'country')
    assert str(tables) == '"user", "country"'


def test_more_tables_with_as(tables):
    tables.set(('user', 'u'), ('country', 'c'))
    assert str(tables) == '"user" AS "u", "country" AS "c"'


def test_simple_as_by_dictionary(tables):
    tables.set({'table': 't1'})
    assert str(tables) == '"table" AS "t1"'


def test_more_tables_with_as_by_dictionary(tables):
    tables.set({'user': 'u', 'country': 'c'})
    assert str(tables) == '"country" AS "c", "user" AS "u"'


def test_more_tables_with_as_by_kwds(tables):
    tables.set(user='u', country='c')
    assert str(tables) == '"country" AS "c", "user" AS "u"'


def test_str(tables):
    tables.set('ščřž')
    assert str(tables) == '"ščřž"'


def test_custom_one_table(tables):
    customsql = sqlpuzzle.customsql('"custom" JOIN "sql"')
    tables.set(customsql)
    assert str(tables) == '"custom" JOIN "sql"'


def test_custom_more_tables(tables):
    customsql = sqlpuzzle.customsql('"custom" JOIN "sql"')
    tables.set(customsql, 'id')
    assert str(tables) == '"custom" JOIN "sql", "id"'


def test_custom_in_column_with_as(tables):
    tables.set({sqlpuzzle.customsql('"custom"'): 'x'})
    assert str(tables) == '"custom" AS "x"'


def test_more_same_tables_print_as_one(tables):
    tables.set('tab', 'tab')
    assert str(tables) == '"tab"'


def test_more_same_tables_with_diff_as_print_as_more(tables):
    tables.set('tab', ('tab', 'tab2'))
    assert str(tables) == '"tab", "tab" AS "tab2"'


def test_copy(tables):
    tables.set('tab')
    copy = tables.copy()
    tables.set('tab2')
    assert str(copy) == '"tab"'
    assert str(tables) == '"tab", "tab2"'


def test_equals(tables):
    tables.set('tab')
    copy = tables.copy()
    assert tables == copy


def test_not_equals(tables):
    tables.set('tab')
    copy = tables.copy()
    tables.set('tab2')
    assert not tables == copy


def test_name_as_integer_exception(tables):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        tables.set(42)


def test_name_as_float_exception(tables):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        tables.set(42.1)


def test_name_as_boolean_exception(tables):
    with pytest.raises(sqlpuzzle.exceptions.InvalidArgumentException):
        tables.set(True)


def testIN(tables):
    tables.set('t1')
    tables.join('t2').on('t2.id', [3, 4])
    assert str(tables) == '"t1" JOIN "t2" ON "t2"."id" IN (3, 4)'


def testGT(tables):
    tables.set('t1')
    tables.join('t2').on('t2.id', sqlpuzzle.relations.GE(42))
    assert str(tables) == '"t1" JOIN "t2" ON "t2"."id" >= 42'


def testInJoin(tables):
    tables.set('t1')
    tables.join({sqlpuzzle.select_from('t2'): 't'}).on('t1.id', 't.id')
    assert str(tables) == '"t1" JOIN (SELECT * FROM "t2") AS "t" ON "t1"."id" = "t"."id"'

def testInCondition(tables):
    tables.set('t1')
    tables.join('t2').on('t2.id', sqlpuzzle.select('id').from_('t3'))
    assert str(tables) == '"t1" JOIN "t2" ON "t2"."id" = (SELECT "id" FROM "t3")'

def testInConditionWithRelationIN(tables):
    tables.set('t1')
    tables.join('t2').on('t2.id', sqlpuzzle.relations.IN(sqlpuzzle.select('id').from_('t3')))
    assert str(tables) == '"t1" JOIN "t2" ON "t2"."id" IN (SELECT "id" FROM "t3")'


def testSimpleJoinNameWithDot1(tables):
    tables.set('t')
    tables.join('a.b').on('t.id', '"a.b".id')
    assert str(tables) == '"t" JOIN "a"."b" ON "t"."id" = "a.b"."id"'


def testSimpleJoinNameWithDot2(tables):
    tables.set('t')
    tables.join('a').on('t.id', 'a."b.id"')
    assert str(tables) == '"t" JOIN "a" ON "t"."id" = "a"."b.id"'


def test_join_without_table_exception(tables):
    with pytest.raises(sqlpuzzle.exceptions.InvalidQueryException):
        tables.join('table')


def test_on_without_join_exception(tables):
    tables.set('table')
    with pytest.raises(sqlpuzzle.exceptions.InvalidQueryException):
        tables.on('a', 'b')


def test_on_without_table_exception(tables):
    with pytest.raises(sqlpuzzle.exceptions.InvalidQueryException):
        tables.on('a', 'b')


class TestSimpleJoins:
    def test_join_without_condition(self, tables):
        tables.set('user').join('user')
        assert str(tables) == '"user" JOIN "user"'

    def test_inner_join(self, tables):
        tables.set('user').inner_join('country').on('user.country_id', 'country.id')
        assert str(tables) == '"user" JOIN "country" ON "user"."country_id" = "country"."id"'

    def test_left_join(self, tables):
        tables.set('user')
        tables.left_join(('user', 'parent')).on('user.parent_id', 'parent.id')
        assert str(tables) == '"user" LEFT JOIN "user" AS "parent" ON "user"."parent_id" = "parent"."id"'

    def test_right_join(self, tables):
        tables.set('t1')
        tables.right_join('t2').on('t1.id', 't2.id')
        assert str(tables) == '"t1" RIGHT JOIN "t2" ON "t1"."id" = "t2"."id"'

    def test_full_join_not_supported(self, tables):
        with pytest.raises(InvalidQueryException):
            tables.set('user').full_join('country').on('user.country_id', 'country.id')

    def test_full_join_supported(self, tables):
        with mock.patch.object(SqlBackend, 'supports_full_join', True):
            tables.set('user').full_join('country').on('user.country_id', 'country.id')
            assert str(tables) == '"user" FULL JOIN "country" ON "user"."country_id" = "country"."id"'

    def test_simple_as_inner_join(self, tables):
        tables.set(('user', 'u')).inner_join(('country', 'c')).on('u.country_id', 'c.id')
        assert str(tables) == '"user" AS "u" JOIN "country" AS "c" ON "u"."country_id" = "c"."id"'

    def test_simple_as_inner_join_by_dictionary(self, tables):
        tables.set({'user': 'u'}).inner_join({'country': 'c'}).on('u.country_id', 'c.id')
        assert str(tables) == '"user" AS "u" JOIN "country" AS "c" ON "u"."country_id" = "c"."id"'

    def test_more_inner_joins(self, tables):
        tables.set('user')
        tables.inner_join('country').on('user.country_id', 'country.id')
        tables.inner_join('role').on('user.role_id', 'role.id')
        assert str(tables) == (
            '"user" JOIN "country" ON "user"."country_id" = "country"."id" '
            'JOIN "role" ON "user"."role_id" = "role"."id"'
        )

    def test_join_with_more_conditions(self, tables):
        tables.set('table')
        tables.left_join('table2').on('table.id', 'table2.id').on('table.id2', 'table2.id2')
        assert str(tables) == (
            '"table" LEFT JOIN "table2" ON "table"."id" = "table2"."id" AND "table"."id2" = "table2"."id2"'
        )

    def test_customsql(self, tables):
        tables.set('t')
        tables.join('u').on('col', sqlpuzzle.customsql('x'))
        assert str(tables) == '"t" JOIN "u" ON "col" = x'

    def test_sqlvalue(self, tables):
        tables.set('t')
        tables.join('u').on('col', sqlpuzzle.V('x'))
        assert str(tables) == '"t" JOIN "u" ON "col" = \'x\''


class TestGroupingJoins:
    def test_left_and_inner_is_inner(self, tables):
        tables.set('t1')
        tables.left_join('t2').on('t1.id', 't2.id')
        tables.join('t2').on('t1.id', 't2.id')
        assert str(tables) == '"t1" JOIN "t2" ON "t1"."id" = "t2"."id"'

    def test_left_and_inner_is_inner_with_reverse_condition(self, tables):
        tables.set('t1')
        tables.left_join('t2').on('t1.id', 't2.id')
        tables.join('t2').on('t2.id', 't1.id')
        assert str(tables) == '"t1" JOIN "t2" ON "t1"."id" = "t2"."id"'

    def test_left_and_inner_is_inner_with_reverse_condition_and_relation(self, tables):
        tables.set('t1')
        tables.left_join('t2').on('t1.id', sqlpuzzle.relations.LE('t2.id'))
        tables.join('t2').on('t2.id', sqlpuzzle.relations.GE('t1.id'))
        assert str(tables) == '"t1" JOIN "t2" ON "t1"."id" <= "t2"."id"'

    def test_left_and_inner_is_inner_with_reverse_condition_but_not_relation(self, tables):
        tables.set('t1')
        tables.left_join('t2').on('t1.id', sqlpuzzle.relations.LE('t2.id'))
        tables.join('t2').on('t2.id', sqlpuzzle.relations.LE('t1.id'))
        assert str(tables) == '"t1" LEFT JOIN "t2" ON "t1"."id" <= "t2"."id" JOIN "t2" ON "t2"."id" <= "t1"."id"'

    def testGroupSameJoins(self, tables):
        tables.set('t1')
        tables.join({'t2': 't'}).on('a', 'b')
        tables.join({'t2': 't'}).on('a', 'b')
        assert str(tables) == '"t1" JOIN "t2" AS "t" ON "a" = "b"'

    def testGroupSameLeftJoins(self, tables):
        tables.set('t1')
        tables.left_join({'t2': 't'}).on('a', 'b')
        tables.left_join({'t2': 't'}).on('a', 'b')
        assert str(tables) == '"t1" LEFT JOIN "t2" AS "t" ON "a" = "b"'

    def testNotGroupWhenConditionIsDifferent(self, tables):
        # When it's different, I don't know what to use. Leave raising exception on database.
        tables.set('t1')
        tables.join({'t2': 't'}).on('a', 'b')
        tables.join({'t2': 't'}).on('c', 'd')
        assert str(tables) == '"t1" JOIN "t2" AS "t" ON "a" = "b" JOIN "t2" AS "t" ON "c" = "d"'


class TestQObject:
    def test_simple_or(self, tables):
        tables.set('t')
        tables.join('a').on(Q(x='y') | Q(y='x'))
        assert str(tables) == '"t" JOIN "a" ON ("x" = \'y\' OR "y" = \'x\')'

    def test_simple_and(self, tables):
        tables.set('t')
        tables.join('a').on(Q(x='y') & Q(y='x'))
        assert str(tables) == '"t" JOIN "a" ON ("x" = \'y\' AND "y" = \'x\')'

    def test_more_complicated(self, tables):
        tables.set('t')
        tables.join('a').on((Q(a=1) & Q(b=2)) | Q(c=3))
        assert str(tables) == '"t" JOIN "a" ON (("a" = 1 AND "b" = 2) OR "c" = 3)'

    def test_more_conditions_in_q(self, tables):
        tables.set('t')
        tables.join('a').on(Q(a=42, b=24) | Q(x='y'))
        assert str(tables) == '"t" JOIN "a" ON (("a" = 42 AND "b" = 24) OR "x" = \'y\')'
