# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle
import sqlPuzzle.relations


class SqlPuzzleTest(unittest.TestCase):
    def testSelectWithoutColumns(self):
        sql = sqlPuzzle.select().from_('user')
        self.assertEqual(str(sql), 'SELECT * FROM `user`')
    
    def testSelectWithColumns(self):
        sql = sqlPuzzle.select('id', 'name').from_('user')
        self.assertEqual(str(sql), 'SELECT `id`, `name` FROM `user`')
    
    def testSelectFrom(self):
        sql = sqlPuzzle.selectFrom('user')
        self.assertEqual(str(sql), 'SELECT * FROM `user`')
    
    def testInsert(self):
        sql = sqlPuzzle.insert().into('user').values(name='Harry')
        self.assertEqual(str(sql), 'INSERT INTO `user` (`name`) VALUES ("Harry")')
    
    def testInsertInto(self):
        sql = sqlPuzzle.insertInto('user').values(name='Harry')
        self.assertEqual(str(sql), 'INSERT INTO `user` (`name`) VALUES ("Harry")')
    
    def testUpdate(self):
        sql = sqlPuzzle.update('user').set(name='Alan').where(id=42)
        self.assertEqual(str(sql), 'UPDATE `user` SET `name` = "Alan" WHERE `id` = 42')
    
    def testDelete(self):
        sql = sqlPuzzle.delete().from_('user').where(id=42)
        self.assertEqual(str(sql), 'DELETE FROM `user` WHERE `id` = 42')
    
    def testDeleteFrom(self):
        sql = sqlPuzzle.deleteFrom('user').where(id=42)
        self.assertEqual(str(sql), 'DELETE FROM `user` WHERE `id` = 42')



testCases = (
    SqlPuzzleTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

