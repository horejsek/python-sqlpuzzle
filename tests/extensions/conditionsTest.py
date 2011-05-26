# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.extensions.conditions
import sqlPuzzle.relations


class ConditionsTest(unittest.TestCase):
    def setUp(self):
        self.conditions = sqlPuzzle.extensions.conditions.Conditions()

    def tearDown(self):
        self.conditions = sqlPuzzle.extensions.conditions.Conditions()
    
    def testWhereByTuple(self):
        self.conditions.where((
            ('name', 'Harry'),
            ('sex', 'female', sqlPuzzle.relations.NOT_EQUAL_TO),
            ('age', 20, sqlPuzzle.relations.GRATHER_THAN),
        ))
        self.assertEqual(str(self.conditions), 'WHERE `name` = "Harry" AND `sex` != "female" AND `age` > 20')
    
    def testWhereByList(self):
        self.conditions.where([
            ['name', 'Harry', sqlPuzzle.relations.LIKE],
            ['sex', 'female', sqlPuzzle.relations.NOT_EQUAL_TO],
            ['age', 20, sqlPuzzle.relations.LESS_TAHN_OR_EQUAL_TO],
        ])
        self.assertEqual(str(self.conditions), 'WHERE `name` LIKE "Harry" AND `sex` != "female" AND `age` <= 20')
    
    def testWhereByDictionary(self):
        self.conditions.where({
            'name': 'Alan',
            'age': 20,
        })
        self.assertEqual(str(self.conditions), 'WHERE `age` = 20 AND `name` = "Alan"')
    
    def testWhereByArgs(self):
        self.conditions.where('age', 20, sqlPuzzle.relations.LESS_THAN)
        self.assertEqual(str(self.conditions), 'WHERE `age` < 20')
    
    def testWhereByKwargs(self):
        self.conditions.where(name='Alan')
        self.assertEqual(str(self.conditions), 'WHERE `name` = "Alan"')
    
    def testSerialWhere(self):
        self.conditions.where(name='Alan')
        self.conditions.where(age=42)
        self.assertEqual(str(self.conditions), 'WHERE `name` = "Alan" AND `age` = 42')
    
    def testRemoveOneCondition(self):
        self.conditions.where(name='Harry', age=20)
        self.conditions.remove('age')
        self.assertEqual(str(self.conditions), 'WHERE `name` = "Harry"')
    
    def testRemoveMoreCondition(self):
        self.conditions.where(name='Harry', age=22, sex='male')
        self.conditions.remove('name', 'sex')
        self.assertEqual(str(self.conditions), 'WHERE `age` = 22')
    
    def testRemoveAllCondition(self):
        self.conditions.where(name='Harry', age=20)
        self.conditions.remove()
        self.assertEqual(str(self.conditions), '')
    
    def testIsSet(self):
        self.assertEqual(self.conditions.isSet(), False)
        self.conditions.where(name='Alan')
        self.assertEqual(self.conditions.isSet(), True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ConditionsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

