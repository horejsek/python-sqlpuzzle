# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._queries.delete


class DeleteTest(unittest.TestCase):
    def setUp(self):
        self.delete = sqlpuzzle._queries.delete.Delete()



class BaseTest(DeleteTest):
    def testSimply(self):
        self.delete.from_('user')
        self.delete.allowDeleteAll()
        self.assertEqual(str(self.delete), 'DELETE FROM `user`')

    def testUnsupportLimit(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.delete.limit, 1)

    def testUnsupportOffset(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.delete.offset, 2)

    def testUnsupportInto(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.delete.into, 'table')

    def testUnsupportValues(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.delete.values, name='Alan')

    def testUnsupportSet(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.delete.set, age=42)



class MoreReferencesTest(DeleteTest):
    def setUp(self):
        super(MoreReferencesTest, self).setUp()
        self.delete.allowDeleteAll()

    def testMoreTables(self):
        self.delete.delete('user').from_('user', 'user2')
        self.assertEqual(str(self.delete), 'DELETE `user` FROM `user`, `user2`')

    def testMoreTablesWithAlias(self):
        self.delete.delete('u').from_({'user': 'u', 'user2': 'u2'})
        self.assertEqual(str(self.delete), 'DELETE `u` FROM `user2` AS `u2`, `user` AS `u`')

    def testJoin(self):
        self.delete.delete('user').from_('user').leftJoin('role').on('role.id', 'user.role_id').where('role.name', ('a', 'b'))
        self.assertEqual(str(self.delete), 'DELETE `user` FROM `user` LEFT JOIN `role` ON (`role`.`id` = `user`.`role_id`) WHERE `role`.`name` IN ("a", "b")')



class WhereTest(DeleteTest):
    def testWhere(self):
        self.delete.from_('user')
        self.delete.where(age=42)
        self.delete.where('name', sqlpuzzle.relations.LIKE('Harry'))
        self.delete.where({
            'sex': 'male',
        })
        self.delete.where((
            ('enabled', 1),
        ))
        self.assertEqual(str(self.delete), 'DELETE FROM `user` WHERE `age` = 42 AND `name` LIKE "Harry" AND `sex` = "male" AND `enabled` = 1')



class CopyTest(WhereTest):
    def testCopy(self):
        self.delete.from_('user').where(id=42)
        copy = self.delete.copy()
        self.delete.where(name='Harry')
        self.assertEqual(str(copy), 'DELETE FROM `user` WHERE `id` = 42')
        self.assertEqual(str(self.delete), 'DELETE FROM `user` WHERE `id` = 42 AND `name` = "Harry"')

    def testEquals(self):
        self.delete.from_('user').where(id=42)
        copy = self.delete.copy()
        self.assertTrue(self.delete == copy)

    def testNotEquals(self):
        self.delete.from_('user').where(id=42)
        copy = self.delete.copy()
        self.delete.where(name='Harry')
        self.assertFalse(self.delete == copy)



testCases = (
    BaseTest,
    MoreReferencesTest,
    WhereTest,
    CopyTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)
