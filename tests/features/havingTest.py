# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import unittest

import sqlpuzzle._features.having
import sqlpuzzle.relations


class HavingTest(unittest.TestCase):
    def setUp(self):
        self.having = sqlpuzzle._features.having.Having()



class BaseTest(HavingTest):
    def testIsNotSet(self):
        self.assertEqual(self.having.isSet(), False)

    def testIsSet(self):
        self.having.where(name='Alan')
        self.assertEqual(self.having.isSet(), True)

    def testWhereByTuple(self):
        self.having.where((
            ('name', 'Harry'),
            ('sex', 'female', sqlpuzzle.relations.NOT_EQUAL_TO),
            ('age', 20, sqlpuzzle.relations.GRATHER_THAN),
        ))
        self.assertEqual(str(self.having), 'HAVING `name` = "Harry" AND `sex` != "female" AND `age` > 20')

    def testWhereByList(self):
        self.having.where([
            ['name', 'Harry', sqlpuzzle.relations.LIKE],
            ['sex', 'female', sqlpuzzle.relations.NOT_EQUAL_TO],
            ['age', 20, sqlpuzzle.relations.LESS_TAHN_OR_EQUAL_TO],
        ])
        self.assertEqual(str(self.having), 'HAVING `name` LIKE "Harry" AND `sex` != "female" AND `age` <= 20')

    def testWhereByDictionary(self):
        self.having.where({
            'name': 'Alan',
            'age': 20,
        })
        self.assertEqual(str(self.having), 'HAVING `age` = 20 AND `name` = "Alan"')

    def testWhereByArgs(self):
        self.having.where('age', 20, sqlpuzzle.relations.LESS_THAN)
        self.assertEqual(str(self.having), 'HAVING `age` < 20')

    def testWhereByKwargs(self):
        self.having.where(name='Alan')
        self.assertEqual(str(self.having), 'HAVING `name` = "Alan"')

    def testSerialWhere(self):
        self.having.where(name='Alan')
        self.having.where(age=42)
        self.assertEqual(str(self.having), 'HAVING `name` = "Alan" AND `age` = 42')



class GroupingTest(HavingTest):
    def testMoreSameConditionsPrintAsOne(self):
        self.having.where(('age', 20), ('age', 20))
        self.assertEqual(str(self.having), 'HAVING `age` = 20')

    def testMoreSameConditionsWithDiffRelationPrintAsMore(self):
        self.having.where(('age', 20), ('age', 20, sqlpuzzle.relations.NE))
        self.assertEqual(str(self.having), 'HAVING `age` = 20 AND `age` != 20')



class AllowedValuesTest(HavingTest):
    def testValueAsInteger(self):
        self.having.where('col', 42)
        self.assertEqual(str(self.having), 'HAVING `col` = 42')

    def testValueAsFloat(self):
        self.having.where('col', 42.1)
        self.assertEqual(str(self.having), 'HAVING `col` = 42.10000')

    def testValueAsBoolean(self):
        self.having.where('col', True)
        self.assertEqual(str(self.having), 'HAVING `col` = 1')

    def testValueAsList(self):
        self.having.where(id=(23, 34, 45))
        self.assertEqual(str(self.having), 'HAVING `id` IN (23, 34, 45)')

    def testValueAsListNotIn(self):
        self.having.where('id', (23, 34, 45), sqlpuzzle.relations.NOT_IN)
        self.assertEqual(str(self.having), 'HAVING `id` NOT IN (23, 34, 45)')



class ExceptionsTest(HavingTest):
    def testColumnAsIntegerException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 42, 'val')

    def testColumnAsFloatException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 42.1, 'val')

    def testColumnAsBooleanException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, True, 'val')

    def testValueAsListWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 'id', (23, 34, 45), sqlpuzzle.relations.LE)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 'id', (23, 34, 45), sqlpuzzle.relations.NE)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 'id', (23, 34, 45), sqlpuzzle.relations.LIKE)

    def testValueAsBooleanWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 'id', True, sqlpuzzle.relations.GT)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 'id', True, sqlpuzzle.relations.NOT_IN)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 'id', True, sqlpuzzle.relations.LIKE)

    def testValueAsIntegerWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 'id', 67, sqlpuzzle.relations.LIKE)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 'id', 67, sqlpuzzle.relations.IN)

    def testValueAsStringWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 'id', 67, sqlpuzzle.relations.NOT_IN)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 'id', 67, sqlpuzzle.relations.IN)

    def testWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.having.where, 'age', 20, 999)



testCases = (
    BaseTest,
    GroupingTest,
    AllowedValuesTest,
    ExceptionsTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)
