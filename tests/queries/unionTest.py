# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._queries.select


class UnionTest(unittest.TestCase):
    def setUp(self):
        self.select1 = sqlpuzzle._queries.select.Select().from_('t1')
        self.select2 = sqlpuzzle._queries.select.Select().from_('t2')



class BaseTest(UnionTest):
    def testUnion(self):
        self.assertEqual(str(self.select1 | self.select2), 'SELECT * FROM `t1` UNION SELECT * FROM `t2`')

    def testUnionAll(self):
        self.assertEqual(str(self.select1 & self.select2), 'SELECT * FROM `t1` UNION ALL SELECT * FROM `t2`')

    def testCombine(self):
        self.assertEqual(str(self.select1 & self.select2 | self.select1), 'SELECT * FROM `t1` UNION ALL SELECT * FROM `t2` UNION SELECT * FROM `t1`')

    def testSubselectInColumnAsUnion(self):
        select = sqlpuzzle.select(self.select1 & self.select2).from_('t')
        self.assertEqual(str(select), 'SELECT (SELECT * FROM `t1` UNION ALL SELECT * FROM `t2`) FROM `t`')

    def testSubselectInTableAsUnion(self):
        select = sqlpuzzle.selectFrom(self.select1 | self.select2)
        self.assertEqual(str(select), 'SELECT * FROM (SELECT * FROM `t1` UNION SELECT * FROM `t2`)')



testCases = (
    BaseTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)
