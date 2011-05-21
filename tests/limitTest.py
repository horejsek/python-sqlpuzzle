# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest
import sqlPuzzle.limit


class LimitTest(unittest.TestCase):
    def setUp(self):
        self.limit = sqlPuzzle.limit.Limit()

    def tearDown(self):
        self.limit = sqlPuzzle.limit.Limit()
    
    def testLimit(self):
        self.limit.limit(10)
        self.assertEqual(str(self.limit), 'LIMIT 10')
    
    def testOffset(self):
        self.limit.limit(10)
        self.limit.offset(50)
        self.assertEqual(str(self.limit), 'LIMIT 10 OFFSET 50')
    
    def testLimitOffset(self):
        self.limit.limit(5, 15)
        self.assertEqual(str(self.limit), 'LIMIT 5 OFFSET 15')
    
    def testInline(self):
        self.limit.limit(3).offset(12)
        self.assertEqual(str(self.limit), 'LIMIT 3 OFFSET 12')
    
    def testInlineInvert(self):
        self.limit.limit(4).offset(16)
        self.assertEqual(str(self.limit), 'LIMIT 4 OFFSET 16')
    
    def testIsSet(self):
        self.assertEqual(self.limit.isSet(), False)
        self.limit.limit(42)
        self.assertEqual(self.limit.isSet(), True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(LimitTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

