from sqlpuzzle._common import SqlReference, check_type_decorator, parse_args
from .queryparts import QueryPart, QueryParts

__all__ = ('Column', 'Columns')


class Column(QueryPart):
    def __init__(self, column_name=None, alias=None):
        super(Column, self).__init__()
        self.column_name = column_name
        self.alias = alias

    def __unicode__(self):
        if self.alias:
            return '%s AS %s' % (
                SqlReference(self.column_name),
                SqlReference(self.alias),
            )
        else:
            return str(SqlReference(self.column_name))

    def __eq__(self, other):
        return (
            type(self) == type(other) and
            self.column_name == other.column_name and
            self.alias == other.alias
        )

    @property
    def column_name(self):
        return self._column_name

    @column_name.setter
    @check_type_decorator((str, int))
    def column_name(self, column_name):
        self._column_name = column_name

    @property
    def alias(self):
        return self._alias

    @alias.setter
    @check_type_decorator((str, type(None)))
    def alias(self, alias):
        self._alias = alias


class Columns(QueryParts):
    _default_query_string = '*'

    def columns(self, *args, **kwds):
        options = {
            'max_items': 2,
            'allow_dict': True,
        }
        for column_name, alias in parse_args(options, *args, **kwds):
            column = Column(column_name, alias)
            if column not in self:
                self.append_part(column)

        return self
