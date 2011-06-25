# -*- coding: utf-8 -*-

import unittest

import queries.deleteTest
import queries.insertTest
import queries.selectTest
import queries.updateTest

import features.columnsTest
import features.groupByTest
import features.havingTest
import features.limitTest
import features.orderByTest
import features.tablesTest
import features.valuesTest
import features.whereTest

import argsParserTest
import sqlPuzzleTest
import sqlValueTest


if __name__ == '__main__':
    testModules = (
        queries.deleteTest,
        queries.insertTest,
        queries.selectTest,
        queries.updateTest,
        
        features.columnsTest,
        features.groupByTest,
        features.havingTest,
        features.limitTest,
        features.orderByTest,
        features.tablesTest,
        features.valuesTest,
        features.whereTest,
        
        argsParserTest,
        sqlValueTest,
        sqlPuzzleTest,
    )
    
    testCases = []
    for testModule in testModules:
        testCases += testModule.testCases

    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=0).run(suite)

