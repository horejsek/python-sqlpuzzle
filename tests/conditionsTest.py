# -*- coding: utf-8 -*-

import unittest
import sqlPuzzle.conditions


class ConditionsTest(unittest.TestCase):
    def setUp(self):
        self.conditions = sqlPuzzle.conditions.Conditions()

    def tearDown(self):
        self.conditions = sqlPuzzle.conditions.Conditions()
    
    def testWhereByTuple(self):
        self.conditions.where((
            ('name', 'Harry'),
            ('sex', 'female', sqlPuzzle.conditions.NOT_EQUAL_TO),
            ('age', 20, sqlPuzzle.conditions.GRATHER_THAN),
        ))
        self.assertEqual(str(self.conditions), 'WHERE `name` = "Harry" AND `sex` != "female" AND `age` > 20')
    
    def testWhereByList(self):
        self.conditions.where([
            ['name', 'Harry', sqlPuzzle.conditions.LIKE],
            ['sex', 'female', sqlPuzzle.conditions.NOT_EQUAL_TO],
            ['age', 20, sqlPuzzle.conditions.LESS_TAHN_OR_EQUAL_TO],
        ])
        self.assertEqual(str(self.conditions), 'WHERE `name` LIKE "Harry" AND `sex` != "female" AND `age` <= 20')
    
    def testWhereByDictionary(self):
        self.conditions.where({
            'name': 'Alan',
            'age': 20,
        })
        self.assertEqual(str(self.conditions), 'WHERE `age` = 20 AND `name` = "Alan"')
    
    def testWhereByArgs(self):
        self.conditions.where('age', 20, sqlPuzzle.conditions.LESS_THAN)
        self.assertEqual(str(self.conditions), 'WHERE `age` < 20')
    
    def testWhereByKwargs(self):
        self.conditions.where(name='Alan')
        self.assertEqual(str(self.conditions), 'WHERE `name` = "Alan"')
    
    def testIsSet(self):
        self.assertEqual(self.conditions.isSet(), False)
        self.conditions.where(name='Alan')
        self.assertEqual(self.conditions.isSet(), True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ConditionsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)


