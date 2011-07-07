# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._queries.select
import sqlpuzzle.relations


class SelectTest(unittest.TestCase):
    def setUp(self):
        self.select = sqlpuzzle._queries.select.Select()

    def tearDown(self):
        self.select = sqlpuzzle._queries.select.Select()



class BaseTest(SelectTest):
    def testSimply(self):
        self.select.columns('id', 'name')
        self.select.from_('user')
        self.assertEqual(str(self.select), 'SELECT `id`, `name` FROM `user`')
    
    def testAllColumns(self):
        self.select.from_('user')
        self.assertEqual(str(self.select), 'SELECT * FROM `user`')
    
    def testAllColumnsFromSpecificTable(self):
        self.select.columns('user.*').from_('user')
        self.assertEqual(str(self.select), 'SELECT `user`.* FROM `user`')
    
    def testOrderBy(self):
        self.select.from_('user')
        self.select.orderBy('id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` ORDER BY `id`')
    
    def testGroupBy(self):
        self.select.from_('user')
        self.select.groupBy('id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` GROUP BY `id`')
    
    def testUnsupportedInto(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.select.into, 'table')
    
    def testUnsupportedValues(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.select.values, name='Alan')
    
    def testUnsupportedSet(self):
        self.assertRaises(sqlpuzzle.exceptions.NotSupprotedException, self.select.set, age=42)



class JoinTest(SelectTest):
    def testJoin(self):
        self.select.from_('user').join('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` JOIN `country` ON (`user`.`country_id` = `country`.`id`)')
    
    def testInnerJoin(self):
        self.select.from_('user').innerJoin('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` JOIN `country` ON (`user`.`country_id` = `country`.`id`)')
    
    def testLeftJoin(self):
        self.select.from_('user').leftJoin('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` LEFT JOIN `country` ON (`user`.`country_id` = `country`.`id`)')
    
    def testRightJoin(self):
        self.select.from_('user').rightJoin('country').on('user.country_id', 'country.id')
        self.assertEqual(str(self.select), 'SELECT * FROM `user` RIGHT JOIN `country` ON (`user`.`country_id` = `country`.`id`)')



class WhereTest(SelectTest):
    def testWhere(self):
        self.select.from_('user')
        self.select.where(age=42)
        self.select.where('name', 'Harry', sqlpuzzle.relations.LIKE)
        self.select.where({
            'sex': 'male',
        })
        self.select.where((
            ('enabled', 1),
        ))
        self.assertEqual(str(self.select), 'SELECT * FROM `user` WHERE `age` = 42 AND `name` LIKE "Harry" AND `sex` = "male" AND `enabled` = 1')



class HavingTest(SelectTest):
    def testWhere(self):
        self.select.from_('user')
        self.select.having(age=42)
        self.select.having('name', 'Harry', sqlpuzzle.relations.LIKE)
        self.select.having({
            'sex': 'male',
        })
        self.select.having((
            ('enabled', 1),
        ))
        self.assertEqual(str(self.select), 'SELECT * FROM `user` HAVING `age` = 42 AND `name` LIKE "Harry" AND `sex` = "male" AND `enabled` = 1')



class LimitTest(SelectTest):
    def testLimit(self):
        self.select.from_('user')
        self.select.limit(10)
        self.assertEqual(str(self.select), 'SELECT * FROM `user` LIMIT 10')
    
    def testLimitWithOffset(self):
        self.select.from_('user')
        self.select.limit(10, 40)
        self.assertEqual(str(self.select), 'SELECT * FROM `user` LIMIT 10 OFFSET 40')
    
    def testLimitOffset(self):
        self.select.from_('user')
        self.select.limit(20)
        self.select.offset(30)
        self.assertEqual(str(self.select), 'SELECT * FROM `user` LIMIT 20 OFFSET 30')



class IntoOutfileTest(SelectTest):
    def setUp(self):
        self.select = sqlpuzzle._queries.select.Select()
        self.select.from_('table')
        self.select.intoOutfile('/tmp/file')
    
    def tearDown(self):
        self.setUp()
    
    def testIntoOutfile(self):
        self.assertEqual(str(self.select), 'SELECT * FROM `table` INTO OUTFILE "/tmp/file"')
    
    def testFieldsTerminatedBy(self):
        self.select.fieldsTerminatedBy(',')
        self.assertEqual(str(self.select), 'SELECT * FROM `table` INTO OUTFILE "/tmp/file" FIELDS TERMINATED BY ","')
    
    def testLinesTerminatedBy(self):
        self.select.linesTerminatedBy('"')
        self.assertEqual(str(self.select), 'SELECT * FROM `table` INTO OUTFILE "/tmp/file" LINES TERMINATED BY "\\""')
    
    def testOptionallyEnclosedBy(self):
        self.select.optionallyEnclosedBy('\n')
        self.assertEqual(str(self.select), 'SELECT * FROM `table` INTO OUTFILE "/tmp/file" OPTIONALLY ENCLOSED BY "\\n"')
    
    def testAllInOne(self):
        self.select.fieldsTerminatedBy(',')
        self.select.linesTerminatedBy('"')
        self.select.optionallyEnclosedBy('\n')
        self.assertEqual(str(self.select), 'SELECT * FROM `table` INTO OUTFILE "/tmp/file" FIELDS TERMINATED BY "," LINES TERMINATED BY "\\"" OPTIONALLY ENCLOSED BY "\\n"')



class SelectOptionsTest(SelectTest):
    def testSqlCache(self):
        self.select.from_('table').sqlCache()
        self.assertEqual(str(self.select), 'SELECT SQL_CACHE * FROM `table`')
    
    def testSqlNoCache(self):
        self.select.from_('table').sqlNoCache()
        self.assertEqual(str(self.select), 'SELECT SQL_NO_CACHE * FROM `table`')
    
    def testAll(self):
        self.select.from_('table').all()
        self.assertEqual(str(self.select), 'SELECT ALL * FROM `table`')
    
    def testDistinct(self):
        self.select.from_('table').distinct()
        self.assertEqual(str(self.select), 'SELECT DISTINCT * FROM `table`')
    
    def testDistinctrow(self):
        self.select.from_('table').distinctrow()
        self.assertEqual(str(self.select), 'SELECT DISTINCTROW * FROM `table`')
    
    def testSqlSmallResult(self):
        self.select.from_('table').sqlSmallResult()
        self.assertEqual(str(self.select), 'SELECT SQL_SMALL_RESULT * FROM `table`')
    
    def testSqlBigResult(self):
        self.select.from_('table').sqlBigResult()
        self.assertEqual(str(self.select), 'SELECT SQL_BIG_RESULT * FROM `table`')
    
    def testSqlBufferResult(self):
        self.select.from_('table').sqlBufferResult()
        self.assertEqual(str(self.select), 'SELECT SQL_BUFFER_RESULT * FROM `table`')
    
    def testSqlCalcFoundRows(self):
        self.select.from_('table').sqlCalcFoundRows()
        self.assertEqual(str(self.select), 'SELECT SQL_CALC_FOUND_ROWS * FROM `table`')
    
    def testStraightJoin(self):
        self.select.from_('table').straightJoin()
        self.assertEqual(str(self.select), 'SELECT STRAIGHT_JOIN * FROM `table`')
    
    def testHighPriority(self):
        self.select.from_('table').highPriority()
        self.assertEqual(str(self.select), 'SELECT HIGH_PRIORITY * FROM `table`')
    
    def testMoreOptions(self):
        self.select.from_('table').distinct().sqlCalcFoundRows().sqlNoCache()
        self.assertEqual(str(self.select), 'SELECT SQL_NO_CACHE SQL_CALC_FOUND_ROWS DISTINCT * FROM `table`')



class UnionTest(SelectTest):
    def testUnion(self):
        self.select.from_('table')
        self.assertEqual(str(self.select | self.select), 'SELECT * FROM `table` UNION SELECT * FROM `table`')
    
    def testUnionAll(self):
        self.select.from_('table')
        self.assertEqual(str(self.select & self.select), 'SELECT * FROM `table` UNION ALL SELECT * FROM `table`')



class SubselectTest(SelectTest):
    def testSubselectInColumns(self):
        subselect = sqlpuzzle._queries.select.Select('col').from_('tab')
        self.select.columns((subselect, 'c'))
        self.select.from_('tab')
        self.assertEqual(str(self.select), 'SELECT (SELECT `col` FROM `tab`) AS "c" FROM `tab`')
    
    def testSubselectInTables(self):
        subselect = sqlpuzzle._queries.select.Select('col').from_('tab')
        self.select.from_((subselect, 't'))
        self.assertEqual(str(self.select), 'SELECT * FROM (SELECT `col` FROM `tab`) AS `t`')
    
    def testSubselectInCondition(self):
        subselect = sqlpuzzle._queries.select.Select('col').from_('tab')
        self.select.from_('tab')
        self.select.where(subselect, 42, sqlpuzzle.relations.LE)
        self.assertEqual(str(self.select), 'SELECT * FROM `tab` WHERE (SELECT `col` FROM `tab`) <= 42')
    
    def testSubselectReference(self):
        subselect = sqlpuzzle._queries.select.Select('col').from_('t1').where('t1.a', '`t2`.a')
        self.select.columns(subselect)
        self.select.from_('t2')
        self.assertEqual(str(self.select), 'SELECT (SELECT `col` FROM `t1` WHERE `t1`.`a` = `t2`.`a`) FROM `t2`')



testCases = (
    BaseTest,
    JoinTest,
    WhereTest,
    LimitTest,
    IntoOutfileTest,
    SelectOptionsTest,
    UnionTest,
    SubselectTest,
)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for testCase in testCases:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

