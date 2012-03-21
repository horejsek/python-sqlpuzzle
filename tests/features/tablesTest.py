# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import unittest

import sqlpuzzle._features.tables


class TablesTest(unittest.TestCase):
    def setUp(self):
        self.tables = sqlpuzzle._features.tables.Tables()



class BaseTest(TablesTest):
    def testIsNotSet(self):
        self.assertEqual(self.tables.isSet(), False)

    def testIsSet(self):
        self.tables.set('table')
        self.assertEqual(self.tables.isSet(), True)

    def testIsSimple(self):
        self.tables.set('table')
        self.assertEqual(self.tables.isSimple(), True)

    def testIsNotSimple(self):
        self.tables.set('table')
        self.tables.join('table2').on('id', 'id2')
        self.assertEqual(self.tables.isSimple(), False)

    def testSimple(self):
        self.tables.set('table')
        self.assertEqual(str(self.tables), '`table`')

    def testSimpleAs(self):
        self.tables.set(('table', 't1'))
        self.assertEqual(str(self.tables), '`table` AS `t1`')

    def testMoreTables(self):
        self.tables.set('user', 'country')
        self.assertEqual(str(self.tables), '`user`, `country`')

    def testMoreTablesWithAs(self):
        self.tables.set(('user', 'u'), ('country', 'c'))
        self.assertEqual(str(self.tables), '`user` AS `u`, `country` AS `c`')

    def testSimpleAsByDictionary(self):
        self.tables.set({'table': 't1'})
        self.assertEqual(str(self.tables), '`table` AS `t1`')

    def testMoreTablesWithAsByDictionary(self):
        self.tables.set({'user': 'u', 'country': 'c'})
        self.assertEqual(str(self.tables), '`country` AS `c`, `user` AS `u`')

    def testMoreTablesWithAsByKwds(self):
        self.tables.set(user='u', country='c')
        self.assertEqual(str(self.tables), '`country` AS `c`, `user` AS `u`')



class CustomSqlTest(TablesTest):
    def setUp(self):
        super(CustomSqlTest, self).setUp()
        self.customSql = sqlpuzzle.customSql('`custom` JOIN `sql`')

    def testOneTable(self):
        self.tables.set(self.customSql)
        self.assertEqual(str(self.tables), '`custom` JOIN `sql`')

    def testMoreTables(self):
        self.tables.set(self.customSql, 'id')
        self.assertEqual(str(self.tables), '`custom` JOIN `sql`, `id`')

    def testCustomInColumnWithAs(self):
        self.tables.set({sqlpuzzle.customSql('`custom`'): 'x'})
        self.assertEqual(str(self.tables), '`custom` AS `x`')



class GroupingTest(TablesTest):
    def testMoreSameTablesPrintAsOne(self):
        self.tables.set('tab', 'tab')
        self.assertEqual(str(self.tables), '`tab`')

    def testMoreSameTablesWithDiffAsPrintAsMore(self):
        self.tables.set('tab', ('tab', 'tab2'))
        self.assertEqual(str(self.tables), '`tab`, `tab` AS `tab2`')



class CopyTest(TablesTest):
    def testCopy(self):
        self.tables.set('tab')
        copy = self.tables.copy()
        self.tables.set('tab2')
        self.assertEqual(str(copy), '`tab`')
        self.assertEqual(str(self.tables), '`tab`, `tab2`')

    def testEquals(self):
        self.tables.set('tab')
        copy = self.tables.copy()
        self.assertTrue(self.tables == copy)

    def testNotEquals(self):
        self.tables.set('tab')
        copy = self.tables.copy()
        self.tables.set('tab2')
        self.assertFalse(self.tables == copy)



class ExceptionsTest(TablesTest):
    def testNameAsIntegerException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.tables.set, 42)

    def testNameAsFloatException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.tables.set, 42.1)

    def testNameAsBooleanException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.tables.set, True)



class SimpleJoinsTest(TablesTest):
    def testInnerJoin(self):
        self.tables.set('user').innerJoin('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.tables), '`user` JOIN `country` ON (`user`.`country_id` = `country`.`id`)')

    def testLeftJoin(self):
        self.tables.set('user')
        self.tables.leftJoin(('user', 'parent')).on('user.parent_id', 'parent.id')
        self.assertEqual(str(self.tables), '`user` LEFT JOIN `user` AS `parent` ON (`user`.`parent_id` = `parent`.`id`)')

    def testRightJoin(self):
        self.tables.set('t1')
        self.tables.rightJoin('t2').on('t1.id', 't2.id')
        self.assertEqual(str(self.tables), '`t1` RIGHT JOIN `t2` ON (`t1`.`id` = `t2`.`id`)')

    def testSimpleAsInnerJoin(self):
        self.tables.set(('user', 'u')).innerJoin(('country', 'c')).on('u.country_id', 'c.id')
        self.assertEqual(str(self.tables), '`user` AS `u` JOIN `country` AS `c` ON (`u`.`country_id` = `c`.`id`)')

    def testSimpleAsInnerJoinByDictionary(self):
        self.tables.set({'user': 'u'}).innerJoin({'country': 'c'}).on('u.country_id', 'c.id')
        self.assertEqual(str(self.tables), '`user` AS `u` JOIN `country` AS `c` ON (`u`.`country_id` = `c`.`id`)')

    def testMoreInnerJoins(self):
        self.tables.set('user')
        self.tables.innerJoin('country').on('user.country_id', 'country.id')
        self.tables.innerJoin('role').on('user.role_id', 'role.id')
        self.assertEqual(str(self.tables), '`user` JOIN `country` ON (`user`.`country_id` = `country`.`id`) JOIN `role` ON (`user`.`role_id` = `role`.`id`)')

    def testJoinWithMoreConditions(self):
        self.tables.set('table')
        self.tables.leftJoin('table2').on('table.id', 'table2.id').on('table.id2', 'table2.id2')
        self.assertEqual(str(self.tables), '`table` LEFT JOIN `table2` ON (`table`.`id` = `table2`.`id` AND `table`.`id2` = `table2`.`id2`)')



class GroupingJoinsTest(TablesTest):
    def testLeftAndInnerIsInner(self):
        self.tables.set('t1')
        self.tables.leftJoin('t2').on('t1.id', 't2.id')
        self.tables.join('t2').on('t1.id', 't2.id')
        self.assertEqual(str(self.tables), '`t1` JOIN `t2` ON (`t1`.`id` = `t2`.`id`)')

    def testLeftAndInnerIsInnerWithReverseCondition(self):
        self.tables.set('t1')
        self.tables.leftJoin('t2').on('t1.id', 't2.id')
        self.tables.join('t2').on('t2.id', 't1.id')
        self.assertEqual(str(self.tables), '`t1` JOIN `t2` ON (`t1`.`id` = `t2`.`id`)')



class BackQuotesJoinsTest(TablesTest):
    def testSimpleJoinNameWithDot1(self):
        self.tables.set('t')
        self.tables.join('a.b').on('t.id', '`a.b`.id')
        self.assertEqual(str(self.tables), '`t` JOIN `a`.`b` ON (`t`.`id` = `a.b`.`id`)')

    def testSimpleJoinNameWithDot2(self):
        self.tables.set('t')
        self.tables.join('a').on('t.id', 'a.`b.id`')
        self.assertEqual(str(self.tables), '`t` JOIN `a` ON (`t`.`id` = `a`.`b.id`)')



class ExceptionsJoinTest(TablesTest):
    def testJoinWithoutOnException(self):
        self.tables.set('table1')
        self.tables.join('table2')
        self.assertRaises(sqlpuzzle.exceptions.InvalidQueryException, str, self.tables)

    def testJoinWithoutTableException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidQueryException, self.tables.join, 'table')

    def testOnWithoutJoinException(self):
        self.tables.set('table')
        self.assertRaises(sqlpuzzle.exceptions.InvalidQueryException, self.tables.on, 'a', 'b')

    def testOnWithoutTableException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidQueryException, self.tables.on, 'a', 'b')



testCases = (
    BaseTest,
    CustomSqlTest,
    GroupingTest,
    ExceptionsTest,
    SimpleJoinsTest,
    GroupingJoinsTest,
    CopyTest,
    BackQuotesJoinsTest,
    ExceptionsJoinTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)
