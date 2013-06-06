# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._queries.insert


class InsertTest(unittest.TestCase):
    def setUp(self):
        self.insert = sqlpuzzle._queries.insert.Insert()



class BaseTest(InsertTest):
    def testSimply(self):
        self.insert.into('user')
        self.insert.values(name='Alan')
        self.assertEqual(str(self.insert), 'INSERT INTO `user` (`name`) VALUES ("Alan")')

    def testUnsupportedFrom(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.insert.from_, 'table')

    def testUnsupportedWhere(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.insert.where, name='Alan')

    def testUnsupportedLimit(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.insert.limit, 1)

    def testUnsupportedOffset(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.insert.offset, 2)

    def testUnsupportedSet(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.insert.set, age=42)



class OnDuplicateKeyUpdateTest(InsertTest):
    def testOnDuplicateKeyUpdate(self):
        self.insert.into('user')
        values = {
            'name': 'Alan',
        }
        self.insert.values(id=1, **values)
        self.insert.onDuplicateKeyUpdate(values)
        self.assertEqual(str(self.insert), 'INSERT INTO `user` (`id`, `name`) VALUES (1, "Alan") ON DUPLICATE KEY UPDATE `name` = "Alan"')



class CopyTest(InsertTest):
    def testCopy(self):
        self.insert.into('user').values(id=1)
        copy = self.insert.copy()
        self.insert.values(id=2)
        self.assertEqual(str(copy), 'INSERT INTO `user` (`id`) VALUES (1)')
        self.assertEqual(str(self.insert), 'INSERT INTO `user` (`id`) VALUES (1), (2)')

    def testEquals(self):
        self.insert.into('user').values(id=1)
        copy = self.insert.copy()
        self.assertTrue(self.insert == copy)

    def testNotEquals(self):
        self.insert.into('user').values(id=1)
        copy = self.insert.copy()
        self.insert.values(name='Alan')
        self.assertFalse(self.insert == copy)



class MultipleInsertTest(InsertTest):
    def test(self):
        self.insert.into('table').values(id=1).values(id=2).values(id=3)
        self.assertEqual(str(self.insert), 'INSERT INTO `table` (`id`) VALUES (1), (2), (3)')



testCases = (
    BaseTest,
    OnDuplicateKeyUpdateTest,
    CopyTest,
    MultipleInsertTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)
