
from six.moves import xrange

import unittest

import sqlpuzzle._features.where
import sqlpuzzle.relations


class WhereTest(unittest.TestCase):
    def setUp(self):
        self.where = sqlpuzzle._features.where.Where()


class BaseTest(WhereTest):
    def test_is_not_set(self):
        self.assertEqual(self.where.is_set(), False)

    def test_is_set(self):
        self.where.where(name='Alan')
        self.assertEqual(self.where.is_set(), True)

    def test_where_by_tuple(self):
        self.where.where((
            ('name', 'Harry'),
            ('sex', sqlpuzzle.relations.NOT_EQUAL_TO('female')),
            ('age', sqlpuzzle.relations.GRATHER_THAN(20)),
        ))
        self.assertEqual(str(self.where), 'WHERE `name` = "Harry" AND `sex` != "female" AND `age` > 20')

    def test_where_by_list(self):
        self.where.where([
            ['name', sqlpuzzle.relations.LIKE('Harry')],
            ['sex', sqlpuzzle.relations.NOT_EQUAL_TO('female')],
            ['age', sqlpuzzle.relations.LESS_TAHN_OR_EQUAL_TO(20)],
        ])
        self.assertEqual(str(self.where), 'WHERE `name` LIKE "Harry" AND `sex` != "female" AND `age` <= 20')

    def test_where_by_dictionary(self):
        self.where.where({
            'name': sqlpuzzle.relations.LIKE('Alan'),
            'age': 20,
        })
        self.assertEqual(str(self.where), 'WHERE `age` = 20 AND `name` LIKE "Alan"')

    def test_where_by_args(self):
        self.where.where('age', sqlpuzzle.relations.LESS_THAN(20))
        self.assertEqual(str(self.where), 'WHERE `age` < 20')

    def test_where_by_kwargs(self):
        self.where.where(name='Alan')
        self.assertEqual(str(self.where), 'WHERE `name` = "Alan"')

    def test_serial_where(self):
        self.where.where(name='Alan')
        self.where.where(age=42)
        self.assertEqual(str(self.where), 'WHERE `name` = "Alan" AND `age` = 42')


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
    def test_one_value(self):
        self.where.where('col', (None,))
        self.assertEqual(str(self.where), 'WHERE `col` IS NULL')

    def test_more_values(self):
        self.where.where('col', ('a', 'b', None))
        self.assertEqual(str(self.where), 'WHERE (`col` IN ("a", "b") OR `col` IS NULL)')


class CustomSqlTest(WhereTest):
    def setUp(self):
        super(CustomSqlTest, self).setUp()
        self.customsql = sqlpuzzle.customsql('`custom` = "sql" OR `sql` = "custom"')

    def test_simple(self):
        self.where.where(self.customsql)
        self.assertEqual(str(self.where), 'WHERE `custom` = "sql" OR `sql` = "custom"')


class GroupingTest(WhereTest):
    def test_more_same_conditions_print_as_one(self):
        self.where.where(('age', 20), ('age', 20))
        self.assertEqual(str(self.where), 'WHERE `age` = 20')

    def test_more_same_conditions_with_diff_relation_print_as_more(self):
        self.where.where(('age', 20), ('age', sqlpuzzle.relations.NE(20)))
        self.assertEqual(str(self.where), 'WHERE `age` = 20 AND `age` != 20')


class AllowedValuesTest(WhereTest):
    def test_value_as_integer(self):
        self.where.where('col', 42)
        self.assertEqual(str(self.where), 'WHERE `col` = 42')

    def test_value_as_float(self):
        self.where.where('col', 42.1)
        self.assertEqual(str(self.where), 'WHERE `col` = 42.10000')

    def test_value_as_boolean(self):
        self.where.where('col', True)
        self.assertEqual(str(self.where), 'WHERE `col` = 1')

    def test_value_as_list(self):
        self.where.where(id=(23, 34, 45))
        self.assertEqual(str(self.where), 'WHERE `id` IN (23, 34, 45)')

    def test_value_as_list_not_in(self):
        self.where.where('id', sqlpuzzle.relations.NOT_IN(23, 34, 45))
        self.assertEqual(str(self.where), 'WHERE `id` NOT IN (23, 34, 45)')

    def test_value_as_generator(self):
        self.where.where('id', (x for x in (23, 34, 45)))
        self.assertEqual(str(self.where), 'WHERE `id` IN (23, 34, 45)')

    def test_value_as_xrange(self):
        self.where.where('id', xrange(3))
        self.assertEqual(str(self.where), 'WHERE `id` IN (0, 1, 2)')

    def test_value_as_none(self):
        self.where.where('country', sqlpuzzle.relations.IS_NOT(None))
        self.assertEqual(str(self.where), 'WHERE `country` IS NOT NULL')


class CopyTest(WhereTest):
    def test_copy(self):
        self.where.where({'id': 42})
        copy = self.where.copy()
        self.where.where({'name': 'Alan'})
        self.assertEqual(str(copy), 'WHERE `id` = 42')
        self.assertEqual(str(self.where), 'WHERE `id` = 42 AND `name` = "Alan"')

    def test_equals(self):
        self.where.where({'id': 42})
        copy = self.where.copy()
        self.assertTrue(self.where == copy)

    def test_not_equals(self):
        self.where.where({'id': 42})
        copy = self.where.copy()
        self.where.where({'name': 'Alan'})
        self.assertFalse(self.where == copy)


class ExceptionsTest(WhereTest):
    def test_column_as_integer_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 42, 'val')

    def test_column_as_float_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, 42.1, 'val')

    def test_column_as_boolean_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, self.where.where, True, 'val')

    def test_value_as_list_wrong_relation_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.LE, (23, 34, 45))
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.NE, (23, 34, 45))
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.LIKE, (23, 34, 45))

    def test_value_as_boolean_wrong_relation_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.GT, True)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.NOT_IN, True)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.LIKE, True)

    def test_value_as_integer_wrong_relation_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.LIKE, 67)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.IN, 67)

    def test_value_as_string_wrong_relation_exception(self):
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.NOT_IN, 67)
        self.assertRaises(sqlpuzzle.exceptions.InvalidArgumentException, sqlpuzzle.relations.IN, 67)
