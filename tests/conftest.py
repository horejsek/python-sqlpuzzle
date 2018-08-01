import pytest

import sqlpuzzle


@pytest.fixture
def sqlite():
    sqlpuzzle.configure('sqlite')
    yield
    sqlpuzzle.configure('sql')


@pytest.fixture
def mysql():
    sqlpuzzle.configure('mysql')
    yield
    sqlpuzzle.configure('sql')


@pytest.fixture
def postgresql():
    sqlpuzzle.configure('postgresql')
    yield
    sqlpuzzle.configure('sql')


@pytest.fixture
def select():
    return sqlpuzzle._queries.select.Select()


@pytest.fixture
def select1():
    return sqlpuzzle._queries.select.Select().from_('t1')


@pytest.fixture
def select2():
    return sqlpuzzle._queries.select.Select().from_('t2')


@pytest.fixture
def insert():
    return sqlpuzzle._queries.insert.Insert()


@pytest.fixture
def update():
    return sqlpuzzle._queries.update.Update()


@pytest.fixture
def delete():
    return sqlpuzzle._queries.delete.Delete()
