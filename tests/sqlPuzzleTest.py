# -*- coding: utf-8 -*-

import unittest
import sqlPuzzle


class SqlPuzzleTest(unittest.TestCase):
    def setUp(self):
        self.sqlPuzzle = sqlPuzzle.SqlPuzzle()

    def tearDown(self):
        self.sqlPuzzle = sqlPuzzle.SqlPuzzle()
    
    def testSelect(self):
        self.sqlPuzzle.select('id', 'name')
        self.sqlPuzzle.from_('user')
        self.assertEqual(self.sqlPuzzle.getQuery(), 'SELECT `id`, `name` FROM `user`')
    
    def testSelectWhere(self):
        self.sqlPuzzle.select('id', 'name')
        self.sqlPuzzle.from_('user')
        self.sqlPuzzle.where('name', 'John', sqlPuzzle.conditions.EQUAL_TO)
        self.assertEqual(self.sqlPuzzle.getQuery(), 'SELECT `id`, `name` FROM `user` WHERE `name` = "John"')
    
    def testSelectLimit(self):
        self.sqlPuzzle.select('id', 'name')
        self.sqlPuzzle.from_('user')
        self.sqlPuzzle.limit(10).offset(100)
        self.assertEqual(self.sqlPuzzle.getQuery(), 'SELECT `id`, `name` FROM `user` LIMIT 10 OFFSET 100')
        
        self.sqlPuzzle.limit(20, 40)
        self.assertEqual(self.sqlPuzzle.getQuery(), 'SELECT `id`, `name` FROM `user` LIMIT 20 OFFSET 40')
        
        self.sqlPuzzle.limit(None)
        self.assertEqual(self.sqlPuzzle.getQuery(), 'SELECT `id`, `name` FROM `user`')
    
    def testInsert(self):
        self.sqlPuzzle.insert().into('user')
        self.sqlPuzzle.values({
            'name': 'Harry',
            'sex': 'female', # :)
        })
        self.assertEqual(self.sqlPuzzle.getQuery(), 'INSERT INTO `user` (`name`, `sex`) VALUES ("Harry", "female")')
        
        self.sqlPuzzle.values(
            name = 'Alan',
            sex = 'male'
        )
        self.assertEqual(self.sqlPuzzle.getQuery(), 'INSERT INTO `user` (`name`, `sex`) VALUES ("Alan", "male")')
    
    def testUpdate(self):
        self.sqlPuzzle.update('user')
        self.sqlPuzzle.set(sex='male')
        self.sqlPuzzle.where(name='Harry')
        self.assertEqual(self.sqlPuzzle.getQuery(), 'UPDATE `user` SET `sex` = "male" WHERE `name` = "Harry"')
        
        self.sqlPuzzle.set({'sex': 'female'})
        self.assertEqual(self.sqlPuzzle.getQuery(), 'UPDATE `user` SET `sex` = "female" WHERE `name` = "Harry"')
    
    def testDelete(self):
        self.sqlPuzzle.delete().from_('user')
        self.sqlPuzzle.where(id=5)
        self.assertEqual(self.sqlPuzzle.getQuery(), 'DELETE FROM `user` WHERE `id` = 5')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SqlPuzzleTest)
    unittest.TextTestRunner(verbosity=2).run(suite)


