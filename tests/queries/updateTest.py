# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import unittest

import sqlpuzzle.exceptions
import sqlpuzzle.queries.update
import sqlpuzzle.relations


class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.update = sqlpuzzle.queries.update.Update()

    def tearDown(self):
        self.update = sqlpuzzle.queries.update.Update()



class BaseTest(UpdateTest):
    def testSimply(self):
        self.update.table('user')
        self.update.set(name='Alan')
        self.update.allowUpdateAll()
        self.assertEqual(str(self.update), 'UPDATE `user` SET `name` = "Alan"')
    
    def testUnsupportedFrom(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.update.from_, 'table')
    
    def testUnsupportedLimit(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.update.limit, 1)
    
    def testUnsupportedOffset(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.update.offset, 2)
    
    def testUnsupportedInto(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.update.into, 'table')
    
    def testUnsupportedValues(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.update.values, name='Alan')



class WhereTest(UpdateTest):
    def testWhere(self):
        self.update.table('user')
        self.update.set(name='Alan')
        self.update.where(age=42)
        self.update.where('name', 'Harry', sqlpuzzle.relations.LIKE)
        self.update.where({
            'sex': 'male',
        })
        self.update.where((
            ('enabled', 1),
        ))
        self.assertEqual(str(self.update), 'UPDATE `user` SET `name` = "Alan" WHERE `age` = 42 AND `name` LIKE "Harry" AND `sex` = "male" AND `enabled` = 1')



testCases = (
    BaseTest,
    WhereTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

