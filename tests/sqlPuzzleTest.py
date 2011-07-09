# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import unittest

import sqlpuzzle
import sqlpuzzle.relations


class SqlPuzzleTest(unittest.TestCase):
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



testCases = (
    SqlPuzzleTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

