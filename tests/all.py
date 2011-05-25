# -*- coding: utf-8 -*-

import unittest

import deleteTest
import insertTest
import selectTest
import updateTest

import columnsTest
import conditionsTest
import groupByTest
import limitTest
import orderByTest
import sqlValueTest
import valuesTest

import sqlPuzzleTest


if __name__ == '__main__':
    objects = (
        deleteTest.DeleteTest,
        insertTest.InsertTest,
        selectTest.SelectTest,
        updateTest.UpdateTest,
        
        columnsTest.ColumnsTest,
        conditionsTest.ConditionsTest,
        groupByTest.GroupByTest,
        limitTest.LimitTest,
        orderByTest.OrderByTest,
        sqlValueTest.SqlValueTest,
        valuesTest.ValuesTest,
        
        sqlPuzzleTest.SqlPuzzleTest,
    )
    
    for object_ in objects:
        suite = unittest.TestLoader().loadTestsFromTestCase(object_)
        unittest.TextTestRunner(verbosity=2).run(suite)

