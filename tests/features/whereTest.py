# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import unittest

import sqlpuzzle._features.where
import sqlpuzzle.relations


class WhereTest(unittest.TestCase):
    def setUp(self):
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
            ('sex', sqlpuzzle.relations.NOT_EQUAL_TO('female')),
            ('age', sqlpuzzle.relations.GRATHER_THAN(20)),
        ))
        self.assertEqual(str(self.where), 'WHERE `name` = "Harry" AND `sex` != "female" AND `age` > 20')

    def testWhereByList(self):
        self.where.where([
            ['name', sqlpuzzle.relations.LIKE('Harry')],
            ['sex', sqlpuzzle.relations.NOT_EQUAL_TO('female')],
            ['age', sqlpuzzle.relations.LESS_TAHN_OR_EQUAL_TO(20)],
        ])
        self.assertEqual(str(self.where), 'WHERE `name` LIKE "Harry" AND `sex` != "female" AND `age` <= 20')

    def testWhereByDictionary(self):
        self.where.where({
            'name': sqlpuzzle.relations.LIKE('Alan'),
            'age': 20,
        })
        self.assertEqual(str(self.where), 'WHERE `age` = 20 AND `name` LIKE "Alan"')

    def testWhereByArgs(self):
        self.where.where('age', sqlpuzzle.relations.LESS_THAN(20))
        self.assertEqual(str(self.where), 'WHERE `age` < 20')

    def testWhereByKwargs(self):
        self.where.where(name='Alan')
        self.assertEqual(str(self.where), 'WHERE `name` = "Alan"')

    def testSerialWhere(self):
        self.where.where(name='Alan')
        self.where.where(age=42)
        self.assertEqual(str(self.where), 'WHERE `name` = "Alan" AND `age` = 42')



# In version 1.0 will be removed.
class OldRelationsTest(WhereTest):
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



class RelationsTest(WhereTest):
    def testEQ(self):
        self.where.where('col', sqlpuzzle.relations.EQ(12))
        self.assertEqual(str(self.where), 'WHERE `col` = 12')

    def testNE(self):
        self.where.where('col', sqlpuzzle.relations.NE(12))
        self.assertEqual(str(self.where), 'WHERE `col` != 12')

    def testGT(self):
        self.where.where('col', sqlpuzzle.relations.GT(12))
        self.assertEqual(str(self.where), 'WHERE `col` > 12')

    def testGE(self):
        self.where.where('col', sqlpuzzle.relations.GE(12))
        self.assertEqual(str(self.where), 'WHERE `col` >= 12')

    def testLT(self):
        self.where.where('col', sqlpuzzle.relations.LT(12))
        self.assertEqual(str(self.where), 'WHERE `col` < 12')

    def testLE(self):
        self.where.where('col', sqlpuzzle.relations.LE(12))
        self.assertEqual(str(self.where), 'WHERE `col` <= 12')

    def testLIKE(self):
        self.where.where('col', sqlpuzzle.relations.LIKE('val'))
        self.assertEqual(str(self.where), 'WHERE `col` LIKE "val"')

    def testREGEXP(self):
        self.where.where('col', sqlpuzzle.relations.REGEXP('val'))
        self.assertEqual(str(self.where), 'WHERE `col` REGEXP "val"')

    def testIN(self):
        self.where.where('col', sqlpuzzle.relations.IN(range(3)))
        self.assertEqual(str(self.where), 'WHERE `col` IN (0, 1, 2)')

    def testNOT_IN(self):
        self.where.where('col', sqlpuzzle.relations.NOT_IN(range(3)))
        self.assertEqual(str(self.where), 'WHERE `col` NOT IN (0, 1, 2)')

    def testIS(self):
        self.where.where('col', sqlpuzzle.relations.IS(None))
        self.assertEqual(str(self.where), 'WHERE `col` IS NULL')

    def testIS_NOT(self):
        self.where.where('col', sqlpuzzle.relations.IS_NOT(None))
        self.assertEqual(str(self.where), 'WHERE `col` IS NOT NULL')



class RelationGeneratorTest(WhereTest):
    def test(self):
        self.where.where('col', (x for x in range(5)))
        self.assertEqual(str(self.where), 'WHERE `col` IN (0, 1, 2, 3, 4)')
        # Second printed version must be same. Generator give values only once!
        self.assertEqual(str(self.where), 'WHERE `col` IN (0, 1, 2, 3, 4)')



class RelationInWithNoneTest(WhereTest):
    def testOneValue(self):
        self.where.where('col', (None,))
        self.assertEqual(str(self.where), 'WHERE `col` IS NULL')

    def testMoreValues(self):
        self.where.where('col', ('a', 'b', None))
        self.assertEqual(str(self.where), 'WHERE (`col` IN ("a", "b") OR `col` IS NULL)')



class CustomSqlTest(WhereTest):
    def setUp(self):
        super(CustomSqlTest, self).setUp()
        self.customSql = sqlpuzzle.customSql('`custom` = "sql" OR `sql` = "custom"')

    def testSimple(self):
        self.where.where(self.customSql)
        self.assertEqual(str(self.where), 'WHERE `custom` = "sql" OR `sql` = "custom"')



class GroupingTest(WhereTest):
    def testMoreSameConditionsPrintAsOne(self):
        self.where.where(('age', 20), ('age', 20))
        self.assertEqual(str(self.where), 'WHERE `age` = 20')

    def testMoreSameConditionsWithDiffRelationPrintAsMore(self):
        self.where.where(('age', 20), ('age', sqlpuzzle.relations.NE(20)))
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
        self.where.where('id', sqlpuzzle.relations.NOT_IN(23, 34, 45))
        self.assertEqual(str(self.where), 'WHERE `id` NOT IN (23, 34, 45)')

    def testValueAsGenerator(self):
        self.where.where('id', (x for x in (23, 34, 45)))
        self.assertEqual(str(self.where), 'WHERE `id` IN (23, 34, 45)')

    def testValueAsXrange(self):
        self.where.where('id', xrange(3))
        self.assertEqual(str(self.where), 'WHERE `id` IN (0, 1, 2)')

    def testValueAsNone(self):
        self.where.where('country', sqlpuzzle.relations.IS_NOT(None))
        self.assertEqual(str(self.where), 'WHERE `country` IS NOT NULL')



class CopyTest(WhereTest):
    def testCopy(self):
        self.where.where({'id': 42})
        copy = self.where.copy()
        self.where.where({'name': 'Alan'})
        self.assertEqual(str(copy), 'WHERE `id` = 42')
        self.assertEqual(str(self.where), 'WHERE `id` = 42 AND `name` = "Alan"')

    def testEquals(self):
        self.where.where({'id': 42})
        copy = self.where.copy()
        self.assertTrue(self.where == copy)

    def testNotEquals(self):
        self.where.where({'id': 42})
        copy = self.where.copy()
        self.where.where({'name': 'Alan'})
        self.assertFalse(self.where == copy)



class ExceptionsTest(WhereTest):
    def testColumnAsIntegerException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 42, 'val')

    def testColumnAsFloatException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 42.1, 'val')

    def testColumnAsBooleanException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, True, 'val')

    def testValueAsListWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.LE, (23, 34, 45))
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.NE, (23, 34, 45))
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.LIKE, (23, 34, 45))

    def testValueAsBooleanWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.GT, True)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.NOT_IN, True)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.LIKE, True)

    def testValueAsIntegerWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.LIKE, 67)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.IN, 67)

    def testValueAsStringWrongRelationException(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.NOT_IN, 67)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.IN, 67)



testCases = (
    BaseTest,
    #OldRelationsTest,
    RelationsTest,
    RelationGeneratorTest,
    RelationInWithNoneTest,
    CustomSqlTest,
    GroupingTest,
    AllowedValuesTest,
    CopyTest,
    ExceptionsTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)
