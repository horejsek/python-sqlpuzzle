
import unittest

import sqlpuzzle.exceptions
import sqlpuzzle._queries.insert


class InsertTest(unittest.TestCase):
    def setUp(self):
        self.insert = sqlpuzzle._queries.insert.Insert()


class BaseTest(InsertTest):
    def test_simply(self):
        self.insert.into('user')
        self.insert.values(name='Alan')
        self.assertEqual(str(self.insert), 'INSERT INTO "user" ("name") VALUES (\'Alan\')')


class OnDuplicateKeyUpdateTest(InsertTest):
    def test_on_duplicate_key_update(self):
        self.insert.into('user')
        values = {
            'name': 'Alan',
        }
        self.insert.values(id=1, **values)
        self.insert.on_duplicate_key_update(values)
        self.assertEqual(str(self.insert), 'INSERT INTO "user" ("id", "name") VALUES (1, \'Alan\') ON DUPLICATE KEY UPDATE "name" = \'Alan\'')


class CopyTest(InsertTest):
    def test_copy(self):
        self.insert.into('user').values(id=1)
        copy = self.insert.copy()
        self.insert.values(id=2)
        self.assertEqual(str(copy), 'INSERT INTO "user" ("id") VALUES (1)')
        self.assertEqual(str(self.insert), 'INSERT INTO "user" ("id") VALUES (1), (2)')

    def test_equals(self):
        self.insert.into('user').values(id=1)
        copy = self.insert.copy()
        self.assertTrue(self.insert == copy)

    def test_not_equals(self):
        self.insert.into('user').values(id=1)
        copy = self.insert.copy()
        self.insert.values(name='Alan')
        self.assertFalse(self.insert == copy)


class MultipleInsertTest(InsertTest):
    def test(self):
        self.insert.into('table').values(id=1).values(id=2).values(id=3)
        self.assertEqual(str(self.insert), 'INSERT INTO "table" ("id") VALUES (1), (2), (3)')
