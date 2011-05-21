# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.conditions
import sqlPuzzle.select
import sqlPuzzle.query


class SelectTest(unittest.TestCase):
    def setUp(self):
        self.select = sqlPuzzle.select.Select()

    def tearDown(self):
        self.select = sqlPuzzle.select.Select()
    
    def testSimply(self):
        self.select.columns('id', 'name')
        self.select.from_('user')
        self.assertEqual(str(self.select), 'SELECT `id`, `name` FROM `user`')
    
    def testAllColumns(self):
        self.select.from_('user')
        self.assertEqual(str(self.select), 'SELECT * FROM `user`')
    
    def testOrderBy(self):
        self.select.from_('user')
        self.select.orderBy('id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` ORDER BY `id`')
    
    def testGroupBy(self):
        self.select.from_('user')
        self.select.groupBy('id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` GROUP BY `id`')
    
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
    
    def testWhere(self):
        self.select.from_('user')
        self.select.where(age=42)
        self.select.where('name', 'Harry', sqlPuzzle.conditions.LIKE)
        self.select.where({
            'sex': 'male',
        })
        self.select.where((
            ('enabled', 1),
        ))
        self.assertEqual(str(self.select), 'SELECT * FROM `user` WHERE `age` = 42 AND `name` LIKE "Harry" AND `sex` = "male" AND `enabled` = 1')
    
    def testUnsupportInto(self):
        self.assertRaises(sqlPuzzle.query.NotSupprotedException, self.select.into, 'table')
    
    def testUnsupportValues(self):
        self.assertRaises(sqlPuzzle.query.NotSupprotedException, self.select.values, name='Alan')
    
    def testUnsupportSet(self):
        self.assertRaises(sqlPuzzle.query.NotSupprotedException, self.select.set, age=42)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SelectTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

