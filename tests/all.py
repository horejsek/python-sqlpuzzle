# -*- coding: utf-8 -*-

import unittest
import sqlPuzzleTest
import conditionsTest
import limitTest


if __name__ == '__main__':
    objects = (
        sqlPuzzleTest.SqlPuzzleTest,
        limitTest.LimitTest,
        conditionsTest.ConditionsTest,
    )
    
    for object_ in objects:
        suite = unittest.TestLoader().loadTestsFromTestCase(object_)
        unittest.TextTestRunner(verbosity=2).run(suite)

