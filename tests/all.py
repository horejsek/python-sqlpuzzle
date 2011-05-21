# -*- coding: utf-8 -*-

import unittest

import deleteTest
import insertTest
import selectTest
import updateTest
import conditionsTest
import groupByTest
import limitTest
import orderByTest
import sqlPuzzleTest


if __name__ == '__main__':
    objects = (
        deleteTest.DeleteTest,
        insertTest.InsertTest,
        selectTest.SelectTest,
        updateTest.UpdateTest,
        
        conditionsTest.ConditionsTest,
        groupByTest.GroupByTest,
        limitTest.LimitTest,
        orderByTest.OrderByTest,
        
        sqlPuzzleTest.SqlPuzzleTest,
    )
    
    for object_ in objects:
        suite = unittest.TestLoader().loadTestsFromTestCase(object_)
        unittest.TextTestRunner(verbosity=2).run(suite)

