# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.exceptions
from sqlPuzzle.argsParser import parseArgsToListOfTuples as parser


class ArgsParserTest(unittest.TestCase):
    def testDefaultArgs1(self):
        self.assertEqual(parser({}, 1), [(1,)])
    
    def testDefaultArgs2(self):
        self.assertEqual(parser({}, 1, 2), [(1,), (2,)])
    
    def testDefaultList(self):
        self.assertEqual(parser({}, [1,]), [(1,)])
    
    def testDefaultTuple(self):
        self.assertEqual(parser({}, (1,)), [(1,)])
    
    def testDefaultKwdsException(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {}, arg=1)
    
    def testDefaultDictionaryException(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {}, {'key': 1})
        
    def testDefaultTooManyException(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {}, (1, 2))
    
    
    def testMax2Args1(self):
        self.assertEqual(parser({'maxItems': 2}, 1), [(1, None)])
    
    def testMax2Args2(self):
        self.assertEqual(parser({'maxItems': 2}, 1, 2), [(1, None), (2, None)])
    
    def testMax2Args3(self):
        self.assertEqual(parser({'maxItems': 2}, 1, 2, 3), [(1, None), (2, None), (3, None)])
    
    def testMax2(self):
        self.assertEqual(parser({'maxItems': 2}, (1, 2), 3), [(1, 2), (3, None)])
    
    
    def testMin2Max1Exception(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {'minItems': 2})
    
    
    def testMin2Args1Exception(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {'minItems': 2, 'maxItems': 2}, 1)
    
    def testMin2Args2Exception(self):
        self.assertEqual(parser({'minItems': 2, 'maxItems': 2}, 1, 2), [(1, 2)])
    
    def testMin2Tuple(self):
        self.assertEqual(parser({'minItems': 2, 'maxItems': 2}, (1, 2)), [(1, 2)])
    
    
    def testAllowDictionaryExceptionTooFew(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {'allowDict': True}, 1)
    
    def testAllowDictionaryException(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {'allowDict': True, 'maxItems': 2}, {'key': 1}, 2)
    
    def testAllowDictionary(self):
        self.assertEqual(parser({'allowDict': True, 'maxItems': 2}, {'key': 1}), [('key', 1)])
    
    def testAllowDictionaryKwds(self):
        self.assertEqual(parser({'allowDict': True, 'maxItems': 2}, key=1), [('key', 1)])
    
    
    def testDictionaryMustByOnlyOneArgumentException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, parser, {'maxItems': 2, 'allowDict': True}, {'key': 'val'}, "some arg")
    
    def testTooFewException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, parser, {'minItems': 2, 'maxItems': 2}, "arg")
    
    def testTooManyException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, parser, {'minItems': 2, 'maxItems': 2}, "arg1", "arg2", "arg3")
    
    def testWrongDatatype(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, parser, {'allowedDataTypes': (int, long, float)}, "string")
    
    
    def testAllowList(self):
        self.assertEqual(parser({'allowList': True}, (1, 2, 3)), [(1,), (2,), (3,)])


testCases = (
    ArgsParserTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

