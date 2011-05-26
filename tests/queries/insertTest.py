# -*- coding: utf-8 -*-
#
# SqlPuzzle
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
    
    def testSimply(self):
        self.insert.into('user')
        self.insert.values(name='Alan')
        self.assertEqual(str(self.insert), 'INSERT INTO `user` (`name`) VALUES ("Alan")')
    
    def testUnsupportFrom(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.insert.from_, 'table')
    
    def testUnsupportWhere(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.insert.where, name='Alan')
    
    def testUnsupportLimit(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.insert.limit, 1)
    
    def testUnsupportOffset(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.insert.offset, 2)
    
    def testUnsupportSet(self):
        self.assertRaises(sqlPuzzle.exceptions.NotSupprotedException, self.insert.set, age=42)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(InsertTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

