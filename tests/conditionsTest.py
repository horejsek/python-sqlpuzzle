# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#
# This application is released under the GNU General Public License
# v3 (or, at your option, any later version). You can find the full
# text of the license under http://www.gnu.org/licenses/gpl.txt.
# By using, editing and/or distributing this software you agree to
# the terms and conditions of this license.
# Thank you for using free software!
#

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

