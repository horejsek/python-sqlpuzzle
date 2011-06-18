# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.exceptions
import sqlPuzzle.queries.delete


class DeleteTest(unittest.TestCase):
    def setUp(self):
        self.delete = sqlPuzzle.queries.delete.Delete()

    def tearDown(self):
        self.delete = sqlPuzzle.queries.delete.Delete()



class BaseTest(DeleteTest):
    def testSimply(self):
        self.delete.from_('user')
        self.delete.allowDeleteAll()
        self.assertEqual(str(self.delete), 'DELETE FROM `user`')
    
    def testUnsupportLimit(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.delete.limit, 1)
    
    def testUnsupportOffset(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.delete.offset, 2)
    
    def testUnsupportInto(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.delete.into, 'table')
    
    def testUnsupportValues(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.delete.values, name='Alan')
    
    def testUnsupportSet(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.delete.set, age=42)



class WhereTest(DeleteTest):
    def testWhere(self):
        self.delete.from_('user')
        self.delete.where(age=42)
        self.delete.where('name', 'Harry', sqlPuzzle.relations.LIKE)
        self.delete.where({
            'sex': 'male',
        })
        self.delete.where((
            ('enabled', 1),
        ))
        self.assertEqual(str(self.delete), 'DELETE FROM `user` WHERE `age` = 42 AND `name` LIKE "Harry" AND `sex` = "male" AND `enabled` = 1')



testCases = (
    BaseTest,
    WhereTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

