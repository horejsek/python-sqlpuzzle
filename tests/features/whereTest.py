# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import unittest

import sqlpuzzle._features.where
import sqlpuzzle.customSql
import sqlpuzzle.relations


class WhereTest(unittest.TestCase):
    def setUp(self):
        self.tearDown()

    def tearDown(self):
        self.where = sqlpuzzle._features.where.Where()



class BaseTest(WhereTest):
    def testIsNotSet(self):
        self.assertEqual(self.where.isSet(), False)
    
    def testIsSet(self):
        self.where.where(name='Alan')
        self.assertEqual(self.where.isSet(), True)
    
    def testWhereByTuple(self):
        self.where.where((
            ('name', 'Harry'),
            ('sex', 'female', sqlpuzzle.relations.NOT_EQUAL_TO),
            ('age', 20, sqlpuzzle.relations.GRATHER_THAN),
        ))
        self.assertEqual(str(self.where), 'WHERE `name` = "Harry" AND `sex` != "female" AND `age` > 20')
    
    def testWhereByList(self):
        self.where.where([
            ['name', 'Harry', sqlpuzzle.relations.LIKE],
            ['sex', 'female', sqlpuzzle.relations.NOT_EQUAL_TO],
            ['age', 20, sqlpuzzle.relations.LESS_TAHN_OR_EQUAL_TO],
        ])
        self.assertEqual(str(self.where), 'WHERE `name` LIKE "Harry" AND `sex` != "female" AND `age` <= 20')
    
    def testWhereByDictionary(self):
        self.where.where({
            'name': 'Alan',
            'age': 20,
        })
        self.assertEqual(str(self.where), 'WHERE `age` = 20 AND `name` = "Alan"')
    
    def testWhereByArgs(self):
        self.where.where('age', 20, sqlpuzzle.relations.LESS_THAN)
        self.assertEqual(str(self.where), 'WHERE `age` < 20')
    
    def testWhereByKwargs(self):
        self.where.where(name='Alan')
        self.assertEqual(str(self.where), 'WHERE `name` = "Alan"')
    
    def testSerialWhere(self):
        self.where.where(name='Alan')
        self.where.where(age=42)
        self.assertEqual(str(self.where), 'WHERE `name` = "Alan" AND `age` = 42')



class RelationsTest(WhereTest):
    def testEQ(self):
        self.where.where('col', 12, sqlpuzzle.relations.EQ)
        self.assertEqual(str(self.where), 'WHERE `col` = 12')
    
    def testNE(self):
        self.where.where('col', 12, sqlpuzzle.relations.NE)
        self.assertEqual(str(self.where), 'WHERE `col` != 12')
    
    def testGT(self):
        self.where.where('col', 12, sqlpuzzle.relations.GT)
        self.assertEqual(str(self.where), 'WHERE `col` > 12')
    
    def testGE(self):
        self.where.where('col', 12, sqlpuzzle.relations.GE)
        self.assertEqual(str(self.where), 'WHERE `col` >= 12')
    
    def testLT(self):
        self.where.where('col', 12, sqlpuzzle.relations.LT)
        self.assertEqual(str(self.where), 'WHERE `col` < 12')
    
    def testLE(self):
        self.where.where('col', 12, sqlpuzzle.relations.LE)
        self.assertEqual(str(self.where), 'WHERE `col` <= 12')
    
    def testLIKE(self):
        self.where.where('col', 'val', sqlpuzzle.relations.LIKE)
        self.assertEqual(str(self.where), 'WHERE `col` LIKE "val"')
    
    def testREGEXP(self):
        self.where.where('col', 'val', sqlpuzzle.relations.REGEXP)
        self.assertEqual(str(self.where), 'WHERE `col` REGEXP "val"')
    
    def testIN(self):
        self.where.where('col', range(3), sqlpuzzle.relations.IN)
        self.assertEqual(str(self.where), 'WHERE `col` IN (0, 1, 2)')
    
    def testNOT_IN(self):
        self.where.where('col', range(3), sqlpuzzle.relations.NOT_IN)
        self.assertEqual(str(self.where), 'WHERE `col` NOT IN (0, 1, 2)')
    
    def testIS(self):
        self.where.where('col', None, sqlpuzzle.relations.IS)
        self.assertEqual(str(self.where), 'WHERE `col` IS NULL')
    
    def testIS_NOT(self):
        self.where.where('col', None, sqlpuzzle.relations.IS_NOT)
        self.assertEqual(str(self.where), 'WHERE `col` IS NOT NULL')



class CustomSqlTest(WhereTest):
    def tearDown(self):
        super(CustomSqlTest, self).tearDown()
        self.customSql = sqlpuzzle.customSql.CustomSql('`custom` = "sql" OR `sql` = "custom"')
    
    def testSimple(self):
        self.where.where(self.customSql)
        self.assertEqual(str(self.where), 'WHERE `custom` = "sql" OR `sql` = "custom"')



class GroupingTest(WhereTest):
    def testMoreSameConditionsPrintAsOne(self):
        self.where.where(('age', 20), ('age', 20))
        self.assertEqual(str(self.where), 'WHERE `age` = 20')
    
    def testMoreSameConditionsWithDiffRelationPrintAsMore(self):
        self.where.where(('age', 20), ('age', 20, sqlpuzzle.relations.NE))
        self.assertEqual(str(self.where), 'WHERE `age` = 20 AND `age` != 20')



class AllowedValuesTest(WhereTest):
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
        self.where.where('id', (23, 34, 45), sqlpuzzle.relations.NOT_IN)
        self.assertEqual(str(self.where), 'WHERE `id` NOT IN (23, 34, 45)')
    
    def testValueAsNone(self):
        self.where.where('country', None, sqlpuzzle.relations.IS_NOT)
        self.assertEqual(str(self.where), 'WHERE `country` IS NOT NULL')



class ExceptionsTest(WhereTest):
    def testColumnAsIntegerException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 42, 'val')
    
    def testColumnAsFloatException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 42.1, 'val')
    
    def testColumnAsBooleanException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, True, 'val')
    
    def testValueAsListWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', (23, 34, 45), sqlpuzzle.relations.LE)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', (23, 34, 45), sqlpuzzle.relations.NE)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', (23, 34, 45), sqlpuzzle.relations.LIKE)
    
    def testValueAsBooleanWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', True, sqlpuzzle.relations.GT)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', True, sqlpuzzle.relations.NOT_IN)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', True, sqlpuzzle.relations.LIKE)
    
    def testValueAsIntegerWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', 67, sqlpuzzle.relations.LIKE)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', 67, sqlpuzzle.relations.IN)
    
    def testValueAsStringWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', 67, sqlpuzzle.relations.NOT_IN)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 'id', 67, sqlpuzzle.relations.IN)
    
    def testWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 'age', 20, 999)



testCases = (
    BaseTest,
    RelationsTest,
    CustomSqlTest,
    GroupingTest,
    AllowedValuesTest,
    ExceptionsTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

