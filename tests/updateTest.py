# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.update
import sqlPuzzle.query


class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.update = sqlPuzzle.update.Update()

    def tearDown(self):
        self.update = sqlPuzzle.update.Update()
    
    def testSimply(self):
        self.update.table('user')
        self.update.set(name='Alan')
        self.assertEqual(str(self.update), 'UPDATE `user` SET `name` = "Alan"')
    
    def testWhere(self):
        self.update.table('user')
        self.update.set(name='Alan')
        self.update.where(age=42)
        self.update.where('name', 'Harry', sqlPuzzle.conditions.LIKE)
        self.update.where({
            'sex': 'male',
        })
        self.update.where((
            ('enabled', 1),
        ))
        self.assertEqual(str(self.update), 'UPDATE `user` SET `name` = "Alan" WHERE `age` = 42 AND `name` LIKE "Harry" AND `sex` = "male" AND `enabled` = 1')
    
    def testUnsupportFrom(self):
        self.assertRaises(sqlPuzzle.query.NotSupprotedException, self.update.from_, 'table')
    
    def testUnsupportLimit(self):
        self.assertRaises(sqlPuzzle.query.NotSupprotedException, self.update.limit, 1)
    
    def testUnsupportOffset(self):
        self.assertRaises(sqlPuzzle.query.NotSupprotedException, self.update.offset, 2)
    
    def testUnsupportInto(self):
        self.assertRaises(sqlPuzzle.query.NotSupprotedException, self.update.into, 'table')
    
    def testUnsupportValues(self):
        self.assertRaises(sqlPuzzle.query.NotSupprotedException, self.update.values, name='Alan')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

