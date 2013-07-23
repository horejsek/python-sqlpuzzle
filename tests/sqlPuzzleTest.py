# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/python-sqlpuzzle
#

import unittest

import sqlpuzzle
import sqlpuzzle.relations


class SqlPuzzleTest(unittest.TestCase):
    def testSelectTest(self):
        sql = sqlpuzzle.select(1)
        self.assertEqual(str(sql), 'SELECT 1')

    def testSelectWithoutColumns(self):
        sql = sqlpuzzle.select().from_('user')
        self.assertEqual(str(sql), 'SELECT * FROM `user`')

    def testSelectWithColumns(self):
        sql = sqlpuzzle.select('id', 'name').from_('user')
        self.assertEqual(str(sql), 'SELECT `id`, `name` FROM `user`')

    def testSelectFrom(self):
        sql = sqlpuzzle.selectFrom('user')
        self.assertEqual(str(sql), 'SELECT * FROM `user`')

    def testSelectFromWithMore(self):
        sql = sqlpuzzle.selectFrom('user', 'country')
        self.assertEqual(str(sql), 'SELECT * FROM `user`, `country`')

    def testInsert(self):
        sql = sqlpuzzle.insert().into('user').values(name='Harry')
        self.assertEqual(str(sql), 'INSERT INTO `user` (`name`) VALUES ("Harry")')

    def testInsertInto(self):
        sql = sqlpuzzle.insertInto('user').values(name='Harry')
        self.assertEqual(str(sql), 'INSERT INTO `user` (`name`) VALUES ("Harry")')

    def testUpdate(self):
        sql = sqlpuzzle.update('user').set(name='Alan').where(id=42)
        self.assertEqual(str(sql), 'UPDATE `user` SET `name` = "Alan" WHERE `id` = 42')

    def testDelete(self):
        sql = sqlpuzzle.delete().from_('user').where(id=42)
        self.assertEqual(str(sql), 'DELETE FROM `user` WHERE `id` = 42')

    def testDeleteFrom(self):
        sql = sqlpuzzle.deleteFrom('user').where(id=42)
        self.assertEqual(str(sql), 'DELETE FROM `user` WHERE `id` = 42')


class CopyTest(unittest.TestCase):
    def testCopy1(self):
        query1 = sqlpuzzle.selectFrom('t').where('c', sqlpuzzle.relations.GT(1))
        query2 = query1.copy()
        self.assertEquals(str(query1), str(query2))

    def testCopyWithCustom(self):
        query1 = sqlpuzzle.selectFrom('t').where(sqlpuzzle.custom('x'))
        query2 = query1.copy()
        self.assertEquals(str(query1), str(query2))


class RelationTest(unittest.TestCase):
    def testCustomSql(self):
        # Not throw exception InvalidArgumentException.
        sqlpuzzle.relations.EQ(sqlpuzzle.customSql('custom'))
        sqlpuzzle.relations.NE(sqlpuzzle.customSql('custom'))
        sqlpuzzle.relations.GT(sqlpuzzle.customSql('custom'))
        sqlpuzzle.relations.GE(sqlpuzzle.customSql('custom'))
        sqlpuzzle.relations.LT(sqlpuzzle.customSql('custom'))
        sqlpuzzle.relations.LE(sqlpuzzle.customSql('custom'))
        sqlpuzzle.relations.LIKE(sqlpuzzle.customSql('custom'))
        sqlpuzzle.relations.REGEXP(sqlpuzzle.customSql('custom'))
        sqlpuzzle.relations.IN(sqlpuzzle.customSql('custom'))
        sqlpuzzle.relations.IN_WITH_NONE(sqlpuzzle.customSql('custom'))
        sqlpuzzle.relations.NOT_IN(sqlpuzzle.customSql('custom'))
        sqlpuzzle.relations.IS(sqlpuzzle.customSql('custom'))
        sqlpuzzle.relations.IS_NOT(sqlpuzzle.customSql('custom'))



testCases = (
    SqlPuzzleTest,
    CopyTest,
    RelationTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)
