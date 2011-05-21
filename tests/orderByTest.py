# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.orderBy


class OrderByTest(unittest.TestCase):
    def setUp(self):
        self.orderBy = sqlPuzzle.orderBy.OrderBy()

    def tearDown(self):
        self.orderBy = sqlPuzzle.orderBy.OrderBy()
    
    def testSimply(self):
        self.orderBy.orderBy('id')
        self.assertEqual(str(self.orderBy), 'ORDER BY `id`')
    
    def testASC(self):
        self.orderBy.orderBy(['name', 'asc'])
        self.assertEqual(str(self.orderBy), 'ORDER BY `name`')
    
    def testDESC(self):
        self.orderBy.orderBy(['name', 'desc'])
        self.assertEqual(str(self.orderBy), 'ORDER BY `name` DESC')
    
    def testMore(self):
        self.orderBy.orderBy('id', ['name', 'desc'])
        self.assertEqual(str(self.orderBy), 'ORDER BY `id`, `name` DESC')
    
    def testIsSet(self):
        self.assertEqual(self.orderBy.isSet(), False)
        self.orderBy.orderBy('id')
        self.assertEqual(self.orderBy.isSet(), True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(OrderByTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

