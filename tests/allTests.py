# -*- coding: utf-8 -*-

import unittest

import queries.deleteTest
import queries.insertTest
import queries.selectTest
import queries.updateTest

import features.columnsTest
import features.conditionsTest
import features.groupByTest
import features.limitTest
import features.orderByTest
import features.tablesTest
import features.valuesTest

import argsParserTest
import sqlPuzzleTest
import sqlValueTest


if __name__ == '__main__':
    testCases = (
        queries.deleteTest.DeleteTest,
        queries.insertTest.InsertTest,
        queries.selectTest.SelectTest,
        queries.updateTest.UpdateTest,
        
        features.columnsTest.ColumnsTest,
        features.conditionsTest.ConditionsTest,
        features.groupByTest.GroupByTest,
        features.limitTest.LimitTest,
        features.orderByTest.OrderByTest,
        features.tablesTest.TablesTest,
        features.valuesTest.ValuesTest,
        
        argsParserTest.ArgsParserTest,
        sqlValueTest.SqlValueTest,
        sqlPuzzleTest.SqlPuzzleTest,
    )

    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=0).run(suite)

