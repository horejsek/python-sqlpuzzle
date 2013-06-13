
import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._queries.select


class UnionTest(unittest.TestCase):
    def setUp(self):
        self.select1 = sqlpuzzle._queries.select.Select().from_('t1')
        self.select2 = sqlpuzzle._queries.select.Select().from_('t2')
        self.union = self.select1 | self.select2


class BaseTest(UnionTest):
    def test_union(self):
        self.assertEqual(str(self.select1 | self.select2), 'SELECT * FROM `t1` UNION SELECT * FROM `t2`')

    def test_union_all(self):
        self.assertEqual(str(self.select1 & self.select2), 'SELECT * FROM `t1` UNION ALL SELECT * FROM `t2`')

    def test_combine(self):
        self.assertEqual(str(self.select1 & self.select2 | self.select1), 'SELECT * FROM `t1` UNION ALL SELECT * FROM `t2` UNION SELECT * FROM `t1`')

    def test_subselect_in_column_as_union(self):
        select = sqlpuzzle.select(self.select1 & self.select2).from_('t')
        self.assertEqual(str(select), 'SELECT (SELECT * FROM `t1` UNION ALL SELECT * FROM `t2`) FROM `t`')

    def test_subselect_in_table_as_union(self):
        select = sqlpuzzle.select_from(self.select1 | self.select2)
        self.assertEqual(str(select), 'SELECT * FROM (SELECT * FROM `t1` UNION SELECT * FROM `t2`)')


class CopyTest(UnionTest):
    def test_copy(self):
        union = self.select1 & self.select2
        copy = union.copy()
        union |= self.select1
        self.assertEqual(str(copy), 'SELECT * FROM `t1` UNION ALL SELECT * FROM `t2`')
        self.assertEqual(str(union), 'SELECT * FROM `t1` UNION ALL SELECT * FROM `t2` UNION SELECT * FROM `t1`')

    def test_equals(self):
        union = self.select1 & self.select2
        copy = union.copy()
        self.assertEqual(str(union), str(copy))

    def test_not_equals(self):
        union = self.select1 & self.select2
        copy = union.copy()
        union |= self.select1
        self.assertFalse(union == copy)
