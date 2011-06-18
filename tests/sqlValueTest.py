# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import datetime
import unittest

from sqlPuzzle.sqlValue import SqlValue


class SqlValueTest(unittest.TestCase):
    def testString(self):
        self.assertEqual(str(SqlValue('Hello World!')), '"Hello World!"')
    
    def testInteger(self):
        self.assertEqual(str(SqlValue(42)), '42')
    
    def testLongInteger(self):
        self.assertEqual(str(SqlValue(123456789012345)), '123456789012345')
    
    def testFloat(self):
        self.assertEqual(str(SqlValue(23.456)), '23.45600')
    
    def testDate(self):
        self.assertEqual(str(SqlValue(datetime.date(2011, 5, 25))), '2011-05-25')
        
    def testDatetime(self):
        self.assertEqual(str(SqlValue(datetime.datetime(2011, 5, 25, 19, 33, 20))), '2011-05-25T19:33:20')


testCases = (
    SqlValueTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

