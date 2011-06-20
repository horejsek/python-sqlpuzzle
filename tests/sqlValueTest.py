# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import datetime
import unittest

import sqlPuzzle
from sqlPuzzle.sqlValue import SqlValue, SqlReference


class SqlValueTest(unittest.TestCase):
    def testString(self):
        self.assertEqual(str(SqlValue('Hello World!')), '"Hello World!"')
    
    def testUnicode(self):
        self.assertEqual(str(SqlValue(u'Hello World!')), '"Hello World!"')
    
    def testInteger(self):
        self.assertEqual(str(SqlValue(42)), '42')
    
    def testLongInteger(self):
        self.assertEqual(str(SqlValue(123456789012345)), '123456789012345')
    
    def testFloat(self):
        self.assertEqual(str(SqlValue(23.456)), '23.45600')
    
    def testBoolean(self):
        self.assertEqual(str(SqlValue(True)), '1')
    
    def testDate(self):
        self.assertEqual(str(SqlValue(datetime.date(2011, 5, 25))), '2011-05-25')
        
    def testDatetime(self):
        self.assertEqual(str(SqlValue(datetime.datetime(2011, 5, 25, 19, 33, 20))), '2011-05-25T19:33:20')
    
    def testListWithString(self):
        self.assertEqual(str(SqlValue(['a', 'b', 'c'])), '("a", "b", "c")')
    
    def testListWithInteger(self):
        self.assertEqual(str(SqlValue([12,23,34])), '(12, 23, 34)')
    
    def testTupleWithInteger(self):
        self.assertEqual(str(SqlValue(('a', 'b', 'c'))), '("a", "b", "c")')
    
    def testTupleWithInteger(self):
        self.assertEqual(str(SqlValue((12,23,34))), '(12, 23, 34)')
    
    def testNone(self):
        self.assertEqual(str(SqlValue(None)), 'NULL')
    
    def testSubselect(self):
        select = sqlPuzzle.selectFrom('table')
        self.assertEqual(str(SqlValue(select)), '(SELECT * FROM `table`)')



class SqlReferenceTest(unittest.TestCase):
    def testString(self):
        self.assertEqual(str(SqlReference('test')), '`test`')
    
    def testUnicode(self):
        self.assertEqual(str(SqlReference(u'test')), '`test`')
    
    def testSubselect(self):
        select = sqlPuzzle.selectFrom('table')
        self.assertEqual(str(SqlReference(select)), '(SELECT * FROM `table`)')
    
    def testTableColumn(self):
        self.assertEqual(str(SqlReference('table.column')), '`table`.`column`')
    
    def testDatabaseTableColumn(self):
        self.assertEqual(str(SqlReference('db.table.column')), '`db`.`table`.`column`')



testCases = (
    SqlValueTest,
    SqlReferenceTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

