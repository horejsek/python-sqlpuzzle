# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.exceptions
import sqlPuzzle.queries.insert


class InsertTest(unittest.TestCase):
    def setUp(self):
        self.insert = sqlPuzzle.queries.insert.Insert()

    def tearDown(self):
        self.insert = sqlPuzzle.queries.insert.Insert()



class BaseTest(InsertTest):
    def testSimply(self):
        self.insert.into('user')
        self.insert.values(name='Alan')
        self.assertEqual(str(self.insert), 'INSERT INTO `user` (`name`) VALUES ("Alan")')
    
    def testUnsupportedFrom(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.insert.from_, 'table')
    
    def testUnsupportedWhere(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.insert.where, name='Alan')
    
    def testUnsupportedLimit(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.insert.limit, 1)
    
    def testUnsupportedOffset(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.insert.offset, 2)
    
    def testUnsupportedSet(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.insert.set, age=42)



class OnDuplicateKeyUpdateTest(InsertTest):
    def testOnDuplicateKeyUpdate(self):
        self.insert.into('user')
        values = {
            'name': 'Alan',
        }
        self.insert.values(id=1).values(values)
        self.insert.onDuplicateKeyUpdate(values)
        self.assertEqual(str(self.insert), 'INSERT INTO `user` (`id`, `name`) VALUES (1, "Alan") ON DUPLICATE KEY UPDATE `name` = "Alan"')



testCases = (
    BaseTest,
    OnDuplicateKeyUpdateTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

