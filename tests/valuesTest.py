# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import unittest

import sqlPuzzle.values


class ValuesTest(unittest.TestCase):
    def setUp(self):
        self.values = sqlPuzzle.values.Values()

    def tearDown(self):
        self.values = sqlPuzzle.values.Values()
    
    def testValuesByTuple(self):
        self.values.set((
            ('name', 'Harry'),
            ('sex', 'female'),
            ('age', 20),
            ('country', None),
        ))
        self.assertEqual(str(self.values), '`country` = NULL, `age` = 20, `name` = "Harry", `sex` = "female"')
    
    def testValuesByList(self):
        self.values.set([
            ['name', 'Harry'],
            ['sex', 'female'],
            ['age', 20],
            ['country', None],
        ])
        self.assertEqual(str(self.values), '`country` = NULL, `age` = 20, `name` = "Harry", `sex` = "female"')
    
    def testValuesByDictionary(self):
        self.values.set({
            'name': 'Alan',
            'age': 20,
        })
        self.assertEqual(str(self.values), '`age` = 20, `name` = "Alan"')
    
    def testValuesByArgs(self):
        self.values.set('age', 20)
        self.assertEqual(str(self.values), '`age` = 20')
    
    def testValuesByKwargs(self):
        self.values.set(name='Alan')
        self.assertEqual(str(self.values), '`name` = "Alan"')
    
    def testIsSet(self):
        self.assertEqual(self.values.isSet(), False)
        self.values.set(id=23)
        self.assertEqual(self.values.isSet(), True)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ValuesTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

