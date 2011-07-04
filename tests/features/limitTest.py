# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._features.limit


class LimitTest(unittest.TestCase):
    def setUp(self):
        self.limit = sqlpuzzle._features.limit.Limit()

    def tearDown(self):
        self.limit = sqlpuzzle._features.limit.Limit()



class BaseTest(LimitTest):
    def testIsNotSet(self):
        self.assertEqual(self.limit.isSet(), False)
    
    def testIsSet(self):
        self.limit.limit(42)
        self.assertEqual(self.limit.isSet(), True)
    
    def testLimit(self):
        self.limit.limit(10)
        self.assertEqual(str(self.limit), 'LIMIT 10')
    
    def testLimitAndOffset(self):
        self.limit.limit(10)
        self.limit.offset(50)
        self.assertEqual(str(self.limit), 'LIMIT 10 OFFSET 50')
    
    def testLimitAndOffsetInOne(self):
        self.limit.limit(5, 15)
        self.assertEqual(str(self.limit), 'LIMIT 5 OFFSET 15')



class InlineTest(LimitTest):
    def testInline(self):
        self.limit.limit(3).offset(12)
        self.assertEqual(str(self.limit), 'LIMIT 3 OFFSET 12')
    
    def testInlineInvert(self):
        self.limit.offset(16).limit(4)
        self.assertEqual(str(self.limit), 'LIMIT 4 OFFSET 16')



class ExceptionsTest(LimitTest):
    def testLimitStringException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.limit.limit, 'limit')
    
    def testLimitFloatException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.limit.limit, 1.2)
    
    def testLimitBooleanException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.limit.limit, False)
    
    def testOffsetStringException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.limit.offset, 'offset')
    
    def testOffsetFloatException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.limit.offset, 1.2)
    
    def testOffsetBooleanException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.limit.offset, False)



testCases = (
    BaseTest,
    InlineTest,
    ExceptionsTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

