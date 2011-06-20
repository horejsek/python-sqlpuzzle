# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.exceptions
import sqlPuzzle.queries.select
import sqlPuzzle.relations


class SelectTest(unittest.TestCase):
    def setUp(self):
        self.select = sqlPuzzle.queries.select.Select()

    def tearDown(self):
        self.select = sqlPuzzle.queries.select.Select()



class BaseTest(SelectTest):
    def testSimply(self):
        self.select.columns('id', 'name')
        self.select.from_('user')
        self.assertEqual(str(self.select), 'SELECT `id`, `name` FROM `user`')
    
    def testAllColumns(self):
        self.select.from_('user')
        self.assertEqual(str(self.select), 'SELECT * FROM `user`')
    
    def testAllColumnsFromSpecificTable(self):
        self.select.columns('user.*').from_('user')
        self.assertEqual(str(self.select), 'SELECT `user`.* FROM `user`')
    
    def testOrderBy(self):
        self.select.from_('user')
        self.select.orderBy('id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` ORDER BY `id`')
    
    def testGroupBy(self):
        self.select.from_('user')
        self.select.groupBy('id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` GROUP BY `id`')
    
    def testUnsupportedInto(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.select.into, 'table')
    
    def testUnsupportedValues(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.select.values, name='Alan')
    
    def testUnsupportedSet(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.select.set, age=42)



class JoinTest(SelectTest):
    def testJoin(self):
        self.select.from_('user').join('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` JOIN `country` ON (`user`.`country_id` = `country`.`id`)')
    
    def testInnerJoin(self):
        self.select.from_('user').innerJoin('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` JOIN `country` ON (`user`.`country_id` = `country`.`id`)')
    
    def testLeftJoin(self):
        self.select.from_('user').leftJoin('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` LEFT JOIN `country` ON (`user`.`country_id` = `country`.`id`)')
    
    def testRightJoin(self):
        self.select.from_('user').rightJoin('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` RIGHT JOIN `country` ON (`user`.`country_id` = `country`.`id`)')



class WhereTest(SelectTest):
    def testWhere(self):
        self.select.from_('user')
        self.select.where(age=42)
        self.select.where('name', 'Harry', sqlPuzzle.relations.LIKE)
        self.select.where({
            'sex': 'male',
        })
        self.select.where((
            ('enabled', 1),
        ))
        self.assertEqual(str(self.select), 'SELECT * FROM `user` WHERE `age` = 42 AND `name` LIKE "Harry" AND `sex` = "male" AND `enabled` = 1')



class LimitTest(SelectTest):
    def testLimit(self):
        self.select.from_('user')
        self.select.limit(10)
        self.assertEqual(str(self.select), 'SELECT * FROM `user` LIMIT 10')
    
    def testLimitWithOffset(self):
        self.select.from_('user')
        self.select.limit(10, 40)
        self.assertEqual(str(self.select), 'SELECT * FROM `user` LIMIT 10 OFFSET 40')
    
    def testLimitOffset(self):
        self.select.from_('user')
        self.select.limit(20)
        self.select.offset(30)
        self.assertEqual(str(self.select), 'SELECT * FROM `user` LIMIT 20 OFFSET 30')



class UnionTest(SelectTest):
    def testUnion(self):
        self.select.from_('table')
        self.assertEqual(self.select | self.select, 'SELECT * FROM `table` UNION SELECT * FROM `table`')
    
    def testUnionAll(self):
        self.select.from_('table')
        self.assertEqual(self.select & self.select, 'SELECT * FROM `table` UNION ALL SELECT * FROM `table`')



class SubselectTest(SelectTest):
    def testSubselectInColumns(self):
        subselect = sqlPuzzle.queries.select.Select('col').from_('tab')
        self.select.columns((subselect, 'c'))
        self.select.from_('tab')
        self.assertEqual(str(self.select), 'SELECT (SELECT `col` FROM `tab`) AS "c" FROM `tab`')
    
    def testSubselectInTables(self):
        subselect = sqlPuzzle.queries.select.Select('col').from_('tab')
        self.select.from_((subselect, 't'))
        self.assertEqual(str(self.select), 'SELECT * FROM (SELECT `col` FROM `tab`) AS `t`')
    
    def testSubselectInCondition(self):
        subselect = sqlPuzzle.queries.select.Select('col').from_('tab')
        self.select.from_('tab')
        self.select.where(subselect, 42, sqlPuzzle.relations.LE)
        self.assertEqual(str(self.select), 'SELECT * FROM `tab` WHERE (SELECT `col` FROM `tab`) <= 42')
    
    def testSubselectReference(self):
        subselect = sqlPuzzle.queries.select.Select('col').from_('t1').where('t1.a', '`t2`.a')
        self.select.columns(subselect)
        self.select.from_('t2')
        self.assertEqual(str(self.select), 'SELECT (SELECT `col` FROM `t1` WHERE `t1`.`a` = `t2`.`a`) FROM `t2`')



testCases = (
    BaseTest,
    JoinTest,
    WhereTest,
    LimitTest,
    UnionTest,
    SubselectTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

