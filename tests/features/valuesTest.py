# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._features.values


class ValuesTest(unittest.TestCase):
    def setUp(self):
        self.values = sqlpuzzle._features.values.Values()

    def tearDown(self):
        self.values = sqlpuzzle._features.values.Values()



class BaseTest(ValuesTest):
    def testIsNotSet(self):
        self.assertEqual(self.values.isSet(), False)
    
    def testIsSet(self):
        self.values.set(id=23)
        self.assertEqual(self.values.isSet(), True)
    
    def testValuesByTuple(self):
        self.values.set((
            ('name', 'Harry'),
            ('sex', 'female'),
            ('age', 20),
            ('country', None),
        ))
        self.assertEqual(str(self.values), '`country` = NULL, `age` = 20, `name` = "Harry", `sex` = "female"')
    
    def testValuesByList(self):
        self.values.set([
            ['name', 'Harry'],
            ['sex', 'female'],
            ['age', 20],
            ['country', None],
        ])
        self.assertEqual(str(self.values), '`country` = NULL, `age` = 20, `name` = "Harry", `sex` = "female"')
    
    def testValuesByDictionary(self):
        self.values.set({
            'name': 'Alan',
            'age': 20,
        })
        self.assertEqual(str(self.values), '`age` = 20, `name` = "Alan"')
    
    def testValuesByArgs(self):
        self.values.set('age', 20)
        self.assertEqual(str(self.values), '`age` = 20')
    
    def testValuesByKwargs(self):
        self.values.set(name='Alan')
        self.assertEqual(str(self.values), '`name` = "Alan"')



class AllowedValuesTest(ValuesTest):
    def testValueAsInteger(self):
        self.values.set('col', 42)
        self.assertEqual(str(self.values), '`col` = 42')
    
    def testValueAsFloat(self):
        self.values.set('col', 42.1)
        self.assertEqual(str(self.values), '`col` = 42.10000')
    
    def testValueAsBoolean(self):
        self.values.set('col', True)
        self.assertEqual(str(self.values), '`col` = 1')



class ExceptionsTest(ValuesTest):
    def testColumnAsIntegerException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.values.set, 42, 'val')
    
    def testColumnAsFloatException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.values.set, 42.1, 'val')
    
    def testColumnAsBooleanException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.values.set, True, 'val')



testCases = (
    BaseTest,
    AllowedValuesTest,
    ExceptionsTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

