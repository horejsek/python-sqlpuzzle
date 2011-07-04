# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.exceptions
from sqlPuzzle.libs.argsParser import parseArgsToListOfTuples as parser


class ArgsParserTest(unittest.TestCase):
    pass



class DefaultTest(ArgsParserTest):
    def testArgs1(self):
        self.assertEqual(parser({}, 1), [(1,)])
    
    def testArgs2(self):
        self.assertEqual(parser({}, 1, 2), [(1,), (2,)])
    
    def testList(self):
        self.assertEqual(parser({}, [1,]), [(1,)])
    
    def testTuple(self):
        self.assertEqual(parser({}, (1,)), [(1,)])




class ExceptionsTest(ArgsParserTest):
    def testKwdsException(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {}, arg=1)
    
    def testDictionaryException(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {}, {'key': 1})
        
    def testTooManyException(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {}, (1, 2))



class OptionMinItemsTest(ArgsParserTest):
    def testMin2Args1Exception(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {'minItems': 2, 'maxItems': 2}, 1)
    
    def testMin2Args2(self):
        self.assertEqual(parser({'minItems': 2, 'maxItems': 2}, 1, 2), [(1, 2)])
    
    def testMin2List(self):
        self.assertEqual(parser({'minItems': 2, 'maxItems': 2}, [1, 2]), [(1, 2)])
    
    def testMin2Tuple(self):
        self.assertEqual(parser({'minItems': 2, 'maxItems': 2}, (1, 2)), [(1, 2)])
    
    def testMinBiggerThanMaxException(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {'minItems': 2})
    
    def testTooFewException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, parser, {'minItems': 2, 'maxItems': 2}, "arg")




class OptionMaxItemsTest(ArgsParserTest):
    def testMax2Args1(self):
        self.assertEqual(parser({'maxItems': 2}, 1), [(1, None)])
    
    def testMax2Args2(self):
        self.assertEqual(parser({'maxItems': 2}, 1, 2), [(1, None), (2, None)])
    
    def testMax2Args3(self):
        self.assertEqual(parser({'maxItems': 2}, 1, 2, 3), [(1, None), (2, None), (3, None)])
    
    def testMax2List(self):
        self.assertEqual(parser({'maxItems': 2}, [1, 2], 3), [(1, 2), (3, None)])
    
    def testMax2Tuple(self):
        self.assertEqual(parser({'maxItems': 2}, (1, 2), 3), [(1, 2), (3, None)])
    
    def testTooManyException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, parser, {'minItems': 2, 'maxItems': 2}, "arg1", "arg2", "arg3")




class OptionAllowDictionaryTest(ArgsParserTest):
    def testArgs(self):
        self.assertEqual(parser({'allowDict': True, 'maxItems': 2}, {'key': 1}), [('key', 1)])
    
    def testKwds(self):
        self.assertEqual(parser({'allowDict': True, 'maxItems': 2}, key=1), [('key', 1)])
    
    def testTooFewException(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {'allowDict': True}, "arg")
    
    def testDictionaryMustBeOnlyOneArgumentException(self):
        self.assertRaises(sqlPuzzle.exceptions.SqlPuzzleException, parser, {'allowDict': True, 'maxItems': 2}, {'key': 1}, "some arg")




class OptionAllowListTest(ArgsParserTest):
    def testArgs(self):
        self.assertEqual(parser({'allowList': True}, 1, 2, 3), [(1,), (2,), (3,)])
    
    def testList(self):
        self.assertEqual(parser({'allowList': True}, (1, 2, 3)), [(1,), (2,), (3,)])




class OptionAllowedDataTypesTest(ArgsParserTest):
    def testSimple(self):
        self.assertEqual(parser({'allowedDataTypes': (int, long, float)}, 2), [(2,)])
    
    def testSimpleExceptions(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, parser, {'allowedDataTypes': (int, long, float)}, "string")
    
    def testSetForEachArgument(self):
        self.assertEqual(parser({'allowedDataTypes': ((int, long, float), (str, unicode)), 'maxItems': 2}, (2, "string")), [(2, "string")])
    
    def testSetForEachArgumentException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, parser, {'allowedDataTypes': ((int, long, float), (str, unicode)), 'maxItems': 2}, ("string", 2))



testCases = (
    DefaultTest,
    ExceptionsTest,
    OptionMinItemsTest,
    OptionMaxItemsTest,
    OptionAllowDictionaryTest,
    OptionAllowListTest,
    OptionAllowedDataTypesTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

