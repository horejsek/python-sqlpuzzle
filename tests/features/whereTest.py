# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.features.where
import sqlPuzzle.relations


class ConditionsTest(unittest.TestCase):
    def setUp(self):
        self.where = sqlPuzzle.features.where.Where()

    def tearDown(self):
        self.where = sqlPuzzle.features.where.Where()



class BaseTest(ConditionsTest):
    def testIsNotSet(self):
        self.assertEqual(self.where.isSet(), False)
    
    def testIsSet(self):
        self.where.where(name='Alan')
        self.assertEqual(self.where.isSet(), True)
    
    def testWhereByTuple(self):
        self.where.where((
            ('name', 'Harry'),
            ('sex', 'female', sqlPuzzle.relations.NOT_EQUAL_TO),
            ('age', 20, sqlPuzzle.relations.GRATHER_THAN),
        ))
        self.assertEqual(str(self.where), 'WHERE `name` = "Harry" AND `sex` != "female" AND `age` > 20')
    
    def testWhereByList(self):
        self.where.where([
            ['name', 'Harry', sqlPuzzle.relations.LIKE],
            ['sex', 'female', sqlPuzzle.relations.NOT_EQUAL_TO],
            ['age', 20, sqlPuzzle.relations.LESS_TAHN_OR_EQUAL_TO],
        ])
        self.assertEqual(str(self.where), 'WHERE `name` LIKE "Harry" AND `sex` != "female" AND `age` <= 20')
    
    def testWhereByDictionary(self):
        self.where.where({
            'name': 'Alan',
            'age': 20,
        })
        self.assertEqual(str(self.where), 'WHERE `age` = 20 AND `name` = "Alan"')
    
    def testWhereByArgs(self):
        self.where.where('age', 20, sqlPuzzle.relations.LESS_THAN)
        self.assertEqual(str(self.where), 'WHERE `age` < 20')
    
    def testWhereByKwargs(self):
        self.where.where(name='Alan')
        self.assertEqual(str(self.where), 'WHERE `name` = "Alan"')
    
    def testSerialWhere(self):
        self.where.where(name='Alan')
        self.where.where(age=42)
        self.assertEqual(str(self.where), 'WHERE `name` = "Alan" AND `age` = 42')



class GroupingTest(ConditionsTest):
    def testMoreSameConditionsPrintAsOne(self):
        self.where.where(('age', 20), ('age', 20))
        self.assertEqual(str(self.where), 'WHERE `age` = 20')
    
    def testMoreSameConditionsWithDiffRelationPrintAsMore(self):
        self.where.where(('age', 20), ('age', 20, sqlPuzzle.relations.NE))
        self.assertEqual(str(self.where), 'WHERE `age` = 20 AND `age` != 20')



class AllowedValuesTest(ConditionsTest):
    def testValueAsInteger(self):
        self.where.where('col', 42)
        self.assertEqual(str(self.where), 'WHERE `col` = 42')
    
    def testValueAsFloat(self):
        self.where.where('col', 42.1)
        self.assertEqual(str(self.where), 'WHERE `col` = 42.10000')
    
    def testValueAsBoolean(self):
        self.where.where('col', True)
        self.assertEqual(str(self.where), 'WHERE `col` = 1')
    
    def testValueAsList(self):
        self.where.where(id=(23, 34, 45))
        self.assertEqual(str(self.where), 'WHERE `id` IN (23, 34, 45)')
    
    def testValueAsListNotIn(self):
        self.where.where('id', (23, 34, 45), sqlPuzzle.relations.NOT_IN)
        self.assertEqual(str(self.where), 'WHERE `id` NOT IN (23, 34, 45)')



class ExceptionsTest(ConditionsTest):
    def testColumnAsIntegerException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, 42, 'val')
    
    def testColumnAsFloatException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, 42.1, 'val')
    
    def testColumnAsBooleanException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, True, 'val')
    
    def testValueAsListWrongRelationException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', (23, 34, 45), sqlPuzzle.relations.LE)
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', (23, 34, 45), sqlPuzzle.relations.NE)
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', (23, 34, 45), sqlPuzzle.relations.LIKE)
    
    def testValueAsBooleanWrongRelationException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', True, sqlPuzzle.relations.GT)
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', True, sqlPuzzle.relations.NOT_IN)
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', True, sqlPuzzle.relations.LIKE)
    
    def testValueAsIntegerWrongRelationException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', 67, sqlPuzzle.relations.LIKE)
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', 67, sqlPuzzle.relations.IN)
    
    def testValueAsStringWrongRelationException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', 67, sqlPuzzle.relations.NOT_IN)
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', 67, sqlPuzzle.relations.IN)
    
    def testWrongRelationException(self):
        self.assertRaises(sqlPuzzle.exceptions.InvalidArgumentException, self.where.where, 'age', 20, 999)



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

