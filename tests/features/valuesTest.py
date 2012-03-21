# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._features.values


class ValuesTest(unittest.TestCase):
    def setUp(self):
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
        self.assertEqual(str(self.values), '`name` = "Harry", `sex` = "female", `age` = 20, `country` = NULL')

    def testValuesByList(self):
        self.values.set([
            ['name', 'Harry'],
            ['sex', 'female'],
            ['age', 20],
            ['country', None],
        ])
        self.assertEqual(str(self.values), '`name` = "Harry", `sex` = "female", `age` = 20, `country` = NULL')

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



class CustomSqlTest(ValuesTest):
    def setUp(self):
        super(CustomSqlTest, self).setUp()
        self.customSql = sqlpuzzle.customSql('`age` = `age` + 1')

    def testSimple(self):
        self.values.set(self.customSql)
        self.assertEqual(str(self.values), '`age` = `age` + 1')



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



class CopyTest(ValuesTest):
    def testCopy(self):
        self.values.set({'id': 42})
        copy = self.values.copy()
        self.values.set({'name': 'Alan'})
        self.assertEqual(str(copy), '`id` = 42')
        self.assertEqual(str(self.values), '`id` = 42, `name` = "Alan"')

    def testEquals(self):
        self.values.set({'id': 42})
        copy = self.values.copy()
        self.assertTrue(self.values == copy)

    def testNotEquals(self):
        self.values.set({'id': 42})
        copy = self.values.copy()
        self.values.set({'name': 'Alan'})
        self.assertFalse(self.values == copy)



class ExceptionsTest(ValuesTest):
    def testColumnAsIntegerException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.values.set, 42, 'val')

    def testColumnAsFloatException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.values.set, 42.1, 'val')

    def testColumnAsBooleanException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.values.set, True, 'val')



testCases = (
    BaseTest,
    CustomSqlTest,
    AllowedValuesTest,
    CopyTest,
    ExceptionsTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)
