# -*- coding: utf-8 -*-

import unittest

import queries.deleteTest
import queries.insertTest
import queries.selectTest
import queries.unionTest
import queries.updateTest

import features.columnsTest
import features.groupByTest
import features.havingTest
import features.limitTest
import features.orderByTest
import features.tablesTest
import features.valuesTest
import features.whereTest

import libs.argsParserTest
import libs.sqlValueTest

import sqlPuzzleTest


testModules = (
    queries.deleteTest,
    queries.insertTest,
    queries.selectTest,
    queries.unionTest,
    queries.updateTest,
    
    features.columnsTest,
    features.groupByTest,
    features.havingTest,
    features.limitTest,
    features.orderByTest,
    features.tablesTest,
    features.valuesTest,
    features.whereTest,
    
    libs.argsParserTest,
    libs.sqlValueTest,
    
    sqlPuzzleTest,
)


# autorun
if __name__ == '__main__':
    testCases = []
    for testModule in testModules:
        testCases += testModule.testCases

    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=0).run(suite)

# for tools
else:
    class UniqName:
        def __init__(self):
            self.__inc = 0
        def __str__(self):
            self.__inc += 1
            return "uniqName_%d" % self.__inc
    uniqName = UniqName()
    
    # all test objects add to the global scope with unique name
    globals_ = globals()
    for testModule in testModules:
        for testCase in testModule.testCases:
            globals()[str(uniqName)] = testCase



