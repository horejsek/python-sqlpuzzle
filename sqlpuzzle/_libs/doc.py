# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

docStrings = {
    'columns': """
        method('id', 'name', ...)
        method(('id', 'asId'), ('name', 'asName'))
        method({'id': 'asId', 'name': 'asName'})
    """,

    'tables': """
        method('user', 'country', ...)
        method(('user', 'asUser'), ('user', 'asParent'))
        method({'user': 'asUser', 'user', 'asParent'})
    """,

    'join': """
        method('table')
        method(('table', 'asTable'))
        method({'table': 'asTable'})
    """,

    'where': """
        method(name='Michael', country=None)
        method({'age': 20, 'enabled': True})
        method('last_modify', datetime.datetime(2011, 6, 15, 22, 11, 00))
        method('id', range(10, 20, 2), sqlpuzzle.relations.IN)
        method([('id', 20), ('name', '%ch%', sqlpuzzle.relation.LIKE)])
    """,

    'limit': """
        method(50) # only limit
        method(50, 200) # limit 50, offset 200
    """,

    'order': """
        Default ordering is ASC.
        method('firstOrderBy', 'secondOrderBy')
        method(('name', 'ASC'), ('last_login', 'DESC'))
        method('country', ('id', DESC))
        method({'name': 'asc', 'surname': 'desc'})
    """,

    'values': """
        method(name='Michael', country=None)
        method({'age': 20, 'enabled': True})
        method('last_modify', datetime.datetime(2011, 6, 15, 22, 11, 00))
        method([('id', 20), ('name', 'Harry')])
    """,
}

def doc(method, feature):
    newDocString = '%s\n%s' % (method.__doc__, docStrings.get(feature, ''))
    newDocString = _stripDocString(newDocString)
    method.__doc__ = newDocString


def _stripDocString(text):
    return "\n".join(line.strip() for line in text.strip().splitlines())
