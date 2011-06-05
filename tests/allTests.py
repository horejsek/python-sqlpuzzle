# -*- coding: utf-8 -*-

import unittest

import queries.deleteTest
import queries.insertTest
import queries.selectTest
import queries.updateTest

import extensions.columnsTest
import extensions.conditionsTest
import extensions.groupByTest
import extensions.limitTest
import extensions.orderByTest
import extensions.tablesTest
import extensions.valuesTest

import argsParserTest
import sqlPuzzleTest
import sqlValueTest


if __name__ == '__main__':
    testCases = (
        queries.deleteTest.DeleteTest,
        queries.insertTest.InsertTest,
        queries.selectTest.SelectTest,
        queries.updateTest.UpdateTest,
        
        extensions.columnsTest.ColumnsTest,
        extensions.conditionsTest.ConditionsTest,
        extensions.groupByTest.GroupByTest,
        extensions.limitTest.LimitTest,
        extensions.orderByTest.OrderByTest,
        extensions.tablesTest.TablesTest,
        extensions.valuesTest.ValuesTest,
        
        argsParserTest.ArgsParserTest,
        sqlValueTest.SqlValueTest,
        sqlPuzzleTest.SqlPuzzleTest,
    )

    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=0).run(suite)

