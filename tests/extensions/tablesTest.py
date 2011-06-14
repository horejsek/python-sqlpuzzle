# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.extensions.tables
import sqlPuzzle.joinTypes


class TablesTest(unittest.TestCase):
    def setUp(self):
        self.tables = sqlPuzzle.extensions.tables.Tables()

    def tearDown(self):
        self.tables = sqlPuzzle.extensions.tables.Tables()
    
    def testSimple(self):
        self.tables.set('table')
        self.assertEqual(str(self.tables), '`table`')
    
    def testSimpleAs(self):
        self.tables.set(('table', 't1'))
        self.assertEqual(str(self.tables), '`table` AS `t1`')
    
    def testSimpleJoinNameWithDot1(self):
        self.tables.set('t')
        self.tables.join('a.b').on('t.id', '`a.b`.id')
        self.assertEqual(str(self.tables), '`t` JOIN `a`.`b` ON (`t`.`id` = `a.b`.`id`)')
    
    def testSimpleJoinNameWithDot2(self):
        self.tables.set('t')
        self.tables.join('a').on('t.id', 'a.`b.id`')
        self.assertEqual(str(self.tables), '`t` JOIN `a` ON (`t`.`id` = `a`.`b.id`)')
    
    def testMoreTables(self):
        self.tables.set('user', 'country')
        self.assertEqual(str(self.tables), '`user`, `country`')
    
    def testMoreTablesWithAs(self):
        self.tables.set(('user', 'u'), ('country', 'c'))
        self.assertEqual(str(self.tables), '`user` AS `u`, `country` AS `c`')
    
    def testSimpleInnerJoin(self):
        self.tables.set('user').innerJoin('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.tables), '`user` JOIN `country` ON (`user`.`country_id` = `country`.`id`)')
    
    def testSimpleAsInnerJoin(self):
        self.tables.set(('user', 'u')).innerJoin(('country', 'c')).on('u.country_id', 'c.id')
        self.assertEqual(str(self.tables), '`user` AS `u` JOIN `country` AS `c` ON (`u`.`country_id` = `c`.`id`)')
    
    def testSimpleMoreInnerJoins(self):
        self.tables.set('user')
        self.tables.innerJoin('country').on('user.country_id', 'country.id')
        self.tables.innerJoin('role').on('user.role_id', 'role.id')
        self.assertEqual(str(self.tables), '`user` JOIN `country` ON (`user`.`country_id` = `country`.`id`) JOIN `role` ON (`user`.`role_id` = `role`.`id`)')
    
    def testLeftJoin(self):
        self.tables.set('user')
        self.tables.leftJoin(('user', 'parent')).on('user.parent_id', 'parent.id')
        self.assertEqual(str(self.tables), '`user` LEFT JOIN `user` AS `parent` ON (`user`.`parent_id` = `parent`.`id`)')
    
    def testRightJoin(self):
        self.tables.set('t1')
        self.tables.rightJoin('t2').on('t1.id', 't2.id')
        self.assertEqual(str(self.tables), '`t1` RIGHT JOIN `t2` ON (`t1`.`id` = `t2`.`id`)')
    
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
    
    def testJoinWithoutOnException(self):
        self.tables.set('table1')
        self.tables.join('table2')
        self.assertRaises(sqlPuzzle.exceptions.InvalidQueryException, str, self.tables)
    
    def testJoinWithoutTableException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidQueryException, self.tables.join, 'table')
    
    def testOnWithoutJoinException(self):
        self.tables.set('table')
        self.assertRaises(sqlPuzzle.exceptions.InvalidQueryException, self.tables.on, 'a', 'b')
    
    def testOnWithoutTableException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidQueryException, self.tables.on, 'a', 'b')
    
    def testMoreSameTablesPrintAsOne(self):
        self.tables.set('tab', 'tab')
        self.assertEqual(str(self.tables), '`tab`')
    
    def testMoreSameTablesWithDiffAsPrintAsMore(self):
        self.tables.set('tab', ('tab', 'tab2'))
        self.assertEqual(str(self.tables), '`tab`, `tab` AS `tab2`')
    
    def testNameAsIntegerException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.tables.set, 42)
    
    def testNameAsFloatException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.tables.set, 42.1)
    
    def testNameAsBooleanException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.tables.set, True)
    
    
    def testIsSet(self):
        self.assertEqual(self.tables.isSet(), False)
        self.tables.set('table')
        self.assertEqual(self.tables.isSet(), True)
    
    def testIsSimple(self):
        self.tables.set('table')
        self.assertEqual(self.tables.isSimple(), True)
        self.tables.join('table2').on('id', 'id2')
        self.assertEqual(self.tables.isSimple(), False)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TablesTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

