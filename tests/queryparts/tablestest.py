# -*- coding: utf-8 -*-

import six

import unittest
try:
    from unittest import mock
except ImportError:
    import mock

import sqlpuzzle
from sqlpuzzle import Q
from sqlpuzzle.exceptions import InvalidQueryException
from sqlpuzzle._backends.sql import SqlBackend
from sqlpuzzle._queryparts import Tables


class TablesTest(unittest.TestCase):
    def setUp(self):
        self.tables = Tables()


class BaseTest(TablesTest):
    def test_is_not_set(self):
        self.assertEqual(self.tables.is_set, False)

    def test_is_set(self):
        self.tables.set('table')
        self.assertEqual(self.tables.is_set, True)

    def test_is_simple(self):
        self.tables.set('table')
        self.assertEqual(self.tables.is_simple(), True)

    def test_is_not_simple(self):
        self.tables.set('table')
        self.tables.join('table2').on('id', 'id2')
        self.assertEqual(self.tables.is_simple(), False)

    def test_simple(self):
        self.tables.set('table')
        self.assertEqual(str(self.tables), '"table"')

    def test_simple_as(self):
        self.tables.set(('table', 't1'))
        self.assertEqual(str(self.tables), '"table" AS "t1"')

    def test_more_tables(self):
        self.tables.set('user', 'country')
        self.assertEqual(str(self.tables), '"user", "country"')

    def test_more_tables_with_as(self):
        self.tables.set(('user', 'u'), ('country', 'c'))
        self.assertEqual(str(self.tables), '"user" AS "u", "country" AS "c"')

    def test_simple_as_by_dictionary(self):
        self.tables.set({'table': 't1'})
        self.assertEqual(str(self.tables), '"table" AS "t1"')

    def test_more_tables_with_as_by_dictionary(self):
        self.tables.set({'user': 'u', 'country': 'c'})
        self.assertEqual(str(self.tables), '"country" AS "c", "user" AS "u"')

    def test_more_tables_with_as_by_kwds(self):
        self.tables.set(user='u', country='c')
        self.assertEqual(str(self.tables), '"country" AS "c", "user" AS "u"')

    def test_str(self):
        self.tables.set('ščřž')
        self.assertEqual(str(self.tables), '"ščřž"')

    def test_unicode(self):
        if six.PY3:
            name = 'ščřž'
        else:
            name = unicode('ščřž', 'utf-8')
        self.tables.set(name)
        self.assertEqual(str(self.tables), '"ščřž"')


class CustomSqlTest(TablesTest):
    def setUp(self):
        super(CustomSqlTest, self).setUp()
        self.customsql = sqlpuzzle.customsql('"custom" JOIN "sql"')

    def test_one_table(self):
        self.tables.set(self.customsql)
        self.assertEqual(str(self.tables), '"custom" JOIN "sql"')

    def test_more_tables(self):
        self.tables.set(self.customsql, 'id')
        self.assertEqual(str(self.tables), '"custom" JOIN "sql", "id"')

    def test_custom_in_column_with_as(self):
        self.tables.set({sqlpuzzle.customsql('"custom"'): 'x'})
        self.assertEqual(str(self.tables), '"custom" AS "x"')



class GroupingTest(TablesTest):
    def test_more_same_tables_print_as_one(self):
        self.tables.set('tab', 'tab')
        self.assertEqual(str(self.tables), '"tab"')

    def test_more_same_tables_with_diff_as_print_as_more(self):
        self.tables.set('tab', ('tab', 'tab2'))
        self.assertEqual(str(self.tables), '"tab", "tab" AS "tab2"')


class CopyTest(TablesTest):
    def test_copy(self):
        self.tables.set('tab')
        copy = self.tables.copy()
        self.tables.set('tab2')
        self.assertEqual(str(copy), '"tab"')
        self.assertEqual(str(self.tables), '"tab", "tab2"')

    def test_equals(self):
        self.tables.set('tab')
        copy = self.tables.copy()
        self.assertTrue(self.tables == copy)

    def test_not_equals(self):
        self.tables.set('tab')
        copy = self.tables.copy()
        self.tables.set('tab2')
        self.assertFalse(self.tables == copy)


class ExceptionsTest(TablesTest):
    def test_name_as_integer_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.tables.set, 42)

    def test_name_as_float_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.tables.set, 42.1)

    def test_name_as_boolean_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.tables.set, True)


class SimpleJoinsTest(TablesTest):
    def test_join_without_condition(self):
        self.tables.set('user').join('user')
        self.assertEqual(str(self.tables), '"user" JOIN "user"')

    def test_inner_join(self):
        self.tables.set('user').inner_join('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.tables), '"user" JOIN "country" ON "user"."country_id" = "country"."id"')

    def test_left_join(self):
        self.tables.set('user')
        self.tables.left_join(('user', 'parent')).on('user.parent_id', 'parent.id')
        self.assertEqual(str(self.tables), '"user" LEFT JOIN "user" AS "parent" ON "user"."parent_id" = "parent"."id"')

    def test_right_join(self):
        self.tables.set('t1')
        self.tables.right_join('t2').on('t1.id', 't2.id')
        self.assertEqual(str(self.tables), '"t1" RIGHT JOIN "t2" ON "t1"."id" = "t2"."id"')

    def test_full_join_not_supported(self):
        with self.assertRaises(InvalidQueryException):
            self.tables.set('user').full_join('country').on('user.country_id', 'country.id')

    def test_full_join_supported(self):
        with mock.patch.object(SqlBackend, 'supports_full_join', True):
            self.tables.set('user').full_join('country').on('user.country_id', 'country.id')
            self.assertEqual(str(self.tables), '"user" FULL JOIN "country" ON "user"."country_id" = "country"."id"')

    def test_simple_as_inner_join(self):
        self.tables.set(('user', 'u')).inner_join(('country', 'c')).on('u.country_id', 'c.id')
        self.assertEqual(str(self.tables), '"user" AS "u" JOIN "country" AS "c" ON "u"."country_id" = "c"."id"')

    def test_simple_as_inner_join_by_dictionary(self):
        self.tables.set({'user': 'u'}).inner_join({'country': 'c'}).on('u.country_id', 'c.id')
        self.assertEqual(str(self.tables), '"user" AS "u" JOIN "country" AS "c" ON "u"."country_id" = "c"."id"')

    def test_more_inner_joins(self):
        self.tables.set('user')
        self.tables.inner_join('country').on('user.country_id', 'country.id')
        self.tables.inner_join('role').on('user.role_id', 'role.id')
        self.assertEqual(str(self.tables), '"user" JOIN "country" ON "user"."country_id" = "country"."id" JOIN "role" ON "user"."role_id" = "role"."id"')

    def test_join_with_more_conditions(self):
        self.tables.set('table')
        self.tables.left_join('table2').on('table.id', 'table2.id').on('table.id2', 'table2.id2')
        self.assertEqual(str(self.tables), '"table" LEFT JOIN "table2" ON "table"."id" = "table2"."id" AND "table"."id2" = "table2"."id2"')

    def test_customsql(self):
        self.tables.set('t')
        self.tables.join('u').on('col', sqlpuzzle.customsql('x'))
        self.assertEqual(str(self.tables), '"t" JOIN "u" ON "col" = x')

    def test_sqlvalue(self):
        self.tables.set('t')
        self.tables.join('u').on('col', sqlpuzzle.V('x'))
        self.assertEqual(str(self.tables), '"t" JOIN "u" ON "col" = \'x\'')


class GroupingJoinsTest(TablesTest):
    def test_left_and_inner_is_inner(self):
        self.tables.set('t1')
        self.tables.left_join('t2').on('t1.id', 't2.id')
        self.tables.join('t2').on('t1.id', 't2.id')
        self.assertEqual(str(self.tables), '"t1" JOIN "t2" ON "t1"."id" = "t2"."id"')

    def test_left_and_inner_is_inner_with_reverse_condition(self):
        self.tables.set('t1')
        self.tables.left_join('t2').on('t1.id', 't2.id')
        self.tables.join('t2').on('t2.id', 't1.id')
        self.assertEqual(str(self.tables), '"t1" JOIN "t2" ON "t1"."id" = "t2"."id"')

    def test_left_and_inner_is_inner_with_reverse_condition_and_relation(self):
        self.tables.set('t1')
        self.tables.left_join('t2').on('t1.id', sqlpuzzle.relations.LE('t2.id'))
        self.tables.join('t2').on('t2.id', sqlpuzzle.relations.GE('t1.id'))
        self.assertEqual(str(self.tables), '"t1" JOIN "t2" ON "t1"."id" <= "t2"."id"')

    def test_left_and_inner_is_inner_with_reverse_condition_but_not_relation(self):
        self.tables.set('t1')
        self.tables.left_join('t2').on('t1.id', sqlpuzzle.relations.LE('t2.id'))
        self.tables.join('t2').on('t2.id', sqlpuzzle.relations.LE('t1.id'))
        self.assertEqual(str(self.tables), '"t1" LEFT JOIN "t2" ON "t1"."id" <= "t2"."id" JOIN "t2" ON "t2"."id" <= "t1"."id"')

    def testGroupSameJoins(self):
        self.tables.set('t1')
        self.tables.join({'t2': 't'}).on('a', 'b')
        self.tables.join({'t2': 't'}).on('a', 'b')
        self.assertEqual(str(self.tables), '"t1" JOIN "t2" AS "t" ON "a" = "b"')

    def testGroupSameLeftJoins(self):
        self.tables.set('t1')
        self.tables.left_join({'t2': 't'}).on('a', 'b')
        self.tables.left_join({'t2': 't'}).on('a', 'b')
        self.assertEqual(str(self.tables), '"t1" LEFT JOIN "t2" AS "t" ON "a" = "b"')

    def testNotGroupWhenConditionIsDifferent(self):
        # When it's different, I don't know what to use. Leave raising exception on database.
        self.tables.set('t1')
        self.tables.join({'t2': 't'}).on('a', 'b')
        self.tables.join({'t2': 't'}).on('c', 'd')
        self.assertEqual(str(self.tables), '"t1" JOIN "t2" AS "t" ON "a" = "b" JOIN "t2" AS "t" ON "c" = "d"')


class JoinWithRelationsTest(TablesTest):
    def testIN(self):
        self.tables.set('t1')
        self.tables.join('t2').on('t2.id', [3, 4])
        self.assertEqual(str(self.tables), '"t1" JOIN "t2" ON "t2"."id" IN (3, 4)')

    def testGT(self):
        self.tables.set('t1')
        self.tables.join('t2').on('t2.id', sqlpuzzle.relations.GE(42))
        self.assertEqual(str(self.tables), '"t1" JOIN "t2" ON "t2"."id" >= 42')


class JoinWithSubselect(TablesTest):
    def testInJoin(self):
        self.tables.set('t1')
        self.tables.join({sqlpuzzle.select_from('t2'): 't'}).on('t1.id', 't.id')
        self.assertEqual(str(self.tables), '"t1" JOIN (SELECT * FROM "t2") AS "t" ON "t1"."id" = "t"."id"')

    def testInCondition(self):
        self.tables.set('t1')
        self.tables.join('t2').on('t2.id', sqlpuzzle.select('id').from_('t3'))
        self.assertEqual(str(self.tables), '"t1" JOIN "t2" ON "t2"."id" = (SELECT "id" FROM "t3")')

    def testInConditionWithRelationIN(self):
        self.tables.set('t1')
        self.tables.join('t2').on('t2.id', sqlpuzzle.relations.IN(sqlpuzzle.select('id').from_('t3')))
        self.assertEqual(str(self.tables), '"t1" JOIN "t2" ON "t2"."id" IN (SELECT "id" FROM "t3")')


class BackQuotesJoinsTest(TablesTest):
    def testSimpleJoinNameWithDot1(self):
        self.tables.set('t')
        self.tables.join('a.b').on('t.id', '"a.b".id')
        self.assertEqual(str(self.tables), '"t" JOIN "a"."b" ON "t"."id" = "a.b"."id"')

    def testSimpleJoinNameWithDot2(self):
        self.tables.set('t')
        self.tables.join('a').on('t.id', 'a."b.id"')
        self.assertEqual(str(self.tables), '"t" JOIN "a" ON "t"."id" = "a"."b.id"')


class ExceptionsJoinTest(TablesTest):
    def test_join_without_table_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidQueryException, self.tables.join, 'table')

    def test_on_without_join_exception(self):
        self.tables.set('table')
        self.assertRaises(sqlpuzzle.exceptions.InvalidQueryException, self.tables.on, 'a', 'b')

    def test_on_without_table_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidQueryException, self.tables.on, 'a', 'b')


class QObjectTest(TablesTest):
    def test_simple_or(self):
        self.tables.set('t')
        self.tables.join('a').on(Q(x='y') | Q(y='x'))
        self.assertEqual(str(self.tables), '"t" JOIN "a" ON ("x" = \'y\' OR "y" = \'x\')')

    def test_simple_and(self):
        self.tables.set('t')
        self.tables.join('a').on(Q(x='y') & Q(y='x'))
        self.assertEqual(str(self.tables), '"t" JOIN "a" ON ("x" = \'y\' AND "y" = \'x\')')

    def test_more_complicated(self):
        self.tables.set('t')
        self.tables.join('a').on((Q(a=1) & Q(b=2)) | Q(c=3))
        self.assertEqual(str(self.tables), '"t" JOIN "a" ON (("a" = 1 AND "b" = 2) OR "c" = 3)')

    def test_more_conditions_in_q(self):
        self.tables.set('t')
        self.tables.join('a').on(Q(a=42, b=24) | Q(x='y'))
        self.assertEqual(str(self.tables), '"t" JOIN "a" ON (("a" = 42 AND "b" = 24) OR "x" = \'y\')')
