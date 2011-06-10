# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle
import sqlPuzzle.relations


class SqlPuzzleTest(unittest.TestCase):
    def testSelect(self):
        sql = sqlPuzzle.select('id', 'name')
        sql.from_('user')
        self.assertEqual(str(sql), 'SELECT `id`, `name` FROM `user`')
    
    def testSelectColumn(self):
        sql = sqlPuzzle.select()
        sql.columns('id', 'name')
        sql.from_('user')
        self.assertEqual(str(sql), 'SELECT `id`, `name` FROM `user`')
    
    def testSelectWhere(self):
        sql = sqlPuzzle.select('id', 'name')
        sql.from_('user')
        sql.where('name', 'John', sqlPuzzle.relations.EQUAL_TO)
        self.assertEqual(str(sql), 'SELECT `id`, `name` FROM `user` WHERE `name` = "John"')
    
    def testSelectLimit(self):
        sql = sqlPuzzle.select('id', 'name')
        sql.from_('user')
        sql.limit(10).offset(100)
        self.assertEqual(str(sql), 'SELECT `id`, `name` FROM `user` LIMIT 10 OFFSET 100')
        
        sql.limit(20, 40)
        self.assertEqual(str(sql), 'SELECT `id`, `name` FROM `user` LIMIT 20 OFFSET 40')
        
        sql.limit(None)
        self.assertEqual(str(sql), 'SELECT `id`, `name` FROM `user`')
    
    def testInsert(self):
        sql = sqlPuzzle.insert().into('user')
        sql.values({
            'name': 'Harry',
            'sex': 'female', # :)
        })
        self.assertEqual(str(sql), 'INSERT INTO `user` (`name`, `sex`) VALUES ("Harry", "female")')
        
        sql.values(
            name = 'Alan',
            sex = 'male'
        )
        self.assertEqual(str(sql), 'INSERT INTO `user` (`name`, `sex`) VALUES ("Alan", "male")')
    
    def testUpdate(self):
        sql = sqlPuzzle.update('user')
        sql.set(sex='male')
        sql.where(name='Harry')
        self.assertEqual(str(sql), 'UPDATE `user` SET `sex` = "male" WHERE `name` = "Harry"')
        
        sql.set({'sex': 'female'})
        self.assertEqual(str(sql), 'UPDATE `user` SET `sex` = "female" WHERE `name` = "Harry"')
    
    def testDelete(self):
        sql = sqlPuzzle.delete().from_('user')
        sql.where(id=5)
        self.assertEqual(str(sql), 'DELETE FROM `user` WHERE `id` = 5')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SqlPuzzleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

