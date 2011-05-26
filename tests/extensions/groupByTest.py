# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.extensions.groupBy


class GroupByTest(unittest.TestCase):
    def setUp(self):
        self.groupBy = sqlPuzzle.extensions.groupBy.GroupBy()

    def tearDown(self):
        self.groupBy = sqlPuzzle.extensions.groupBy.GroupBy()
    
    def testSimply(self):
        self.groupBy.groupBy('id')
        self.assertEqual(str(self.groupBy), 'GROUP BY `id`')
    
    def testASC(self):
        self.groupBy.groupBy(['name', 'asc'])
        self.assertEqual(str(self.groupBy), 'GROUP BY `name`')
    
    def testDESC(self):
        self.groupBy.groupBy(['name', 'desc'])
        self.assertEqual(str(self.groupBy), 'GROUP BY `name` DESC')
    
    def testMore(self):
        self.groupBy.groupBy('id', ['name', 'desc'])
        self.assertEqual(str(self.groupBy), 'GROUP BY `id`, `name` DESC')
    
    def testIsSet(self):
        self.assertEqual(self.groupBy.isSet(), False)
        self.groupBy.groupBy('id')
        self.assertEqual(self.groupBy.isSet(), True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GroupByTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

