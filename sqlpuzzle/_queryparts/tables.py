import sqlpuzzle
from sqlpuzzle._backends import get_backend
from sqlpuzzle._common import SqlValue, SqlReference, force_text, check_type_decorator, parse_args
from sqlpuzzle.exceptions import InvalidArgumentException, InvalidQueryException
from .queryparts import QueryPart, QueryParts
from .conditions import Condition, Conditions

__all__ = ('Table', 'Tables', 'TablesForSelect')


INNER_JOIN = 0
LEFT_JOIN = 1
RIGHT_JOIN = 2
FULL_JOIN = 3

JOIN_TYPES = {
    INNER_JOIN: 'JOIN',
    LEFT_JOIN: 'LEFT JOIN',
    RIGHT_JOIN: 'RIGHT JOIN',
    FULL_JOIN: 'FULL JOIN',
}


class OnCondition(Condition):
    _revert_relation_map = {
        sqlpuzzle.relations.EQ: sqlpuzzle.relations.EQ,
        sqlpuzzle.relations.NE: sqlpuzzle.relations.NE,
        sqlpuzzle.relations.GT: sqlpuzzle.relations.LT,
        sqlpuzzle.relations.GE: sqlpuzzle.relations.LE,
        sqlpuzzle.relations.LT: sqlpuzzle.relations.GT,
        sqlpuzzle.relations.LE: sqlpuzzle.relations.GE,
    }

    def __eq__(self, other):
        if super().__eq__(other):
            return True

        #  Condition can be:
        #   t1.id=t2.id and t2.id=t1.id => true (conditions are same)
        #   t1.id>t2.id and t2.id<t1.id => true (conditions are same)
        #   t1.id>t2.id and t2.id>t1.id => false (conditions are not same)
        #  But only if value is string, because only string is reference.
        #+ Value and reference can not be mixed. Therefore this condition
        #+ is only here for tables and not for all condition. Only here is
        #+ string manipulated as reference.
        revert_relation = self._revert_relation_map.get(type(self.relation_instance), None)
        return (
            type(self) == type(other)
            and isinstance(self.value, str)
            and self.value == other.column_name
            and self.column_name == other.value
            and revert_relation == type(other.relation_instance)
        )

    def __str__(self):
        value_transformer = SqlReference if isinstance(self.value, str) else SqlValue
        return self._value._format_condition(SqlReference(self.column_name), value_transformer=value_transformer)


class OnConditions(Conditions):
    _condition_class = OnCondition


class Table(QueryPart):
    def __init__(self, table_name=None, alias=None):
        super().__init__()
        self.table_name = table_name
        self.alias = alias
        self._joins = []

    def __str__(self):
        if self.alias:
            table = '{} AS {}'.format(
                SqlReference(self.table_name),
                SqlReference(self.alias),
            )
        else:
            table = force_text(SqlReference(self.table_name))

        if self._joins:
            self._minimize_joins()
            table += ' ' + ' '.join(
                '{} {}{}'.format(
                    JOIN_TYPES[join['type']],
                    join['table'],
                    ' ON {}'.format(join['ons']) if join['ons'].is_set else '',
                ) for join in self._joins
            )

        return table

    def __eq__(self, other):
        return (
            type(self) == type(other) and
            self.table_name == other.table_name and
            self.alias == other.alias and
            self._joins == other._joins
        )

    @property
    def table_name(self):
        return self._table_name

    @table_name.setter
    @check_type_decorator(str)
    def table_name(self, table_name):
        self._table_name = table_name

    @property
    def alias(self):
        return self._alias

    @alias.setter
    @check_type_decorator((type(None), str))
    def alias(self, alias):
        self._alias = alias

    def is_simple(self):
        """Is it table without any join?"""
        return self._joins == []

    def join(self, arg, join_type=INNER_JOIN):
        if isinstance(arg, (list, tuple)) and len(arg) == 2:
            table = Table(*arg)
        elif isinstance(arg, dict) and len(arg) == 1:
            table = Table(*arg.popitem())
        elif isinstance(arg, str):
            table = Table(arg)
        else:
            raise InvalidArgumentException('Invalid argument "{}" for join.'.format(arg))

        self._joins.append({
            'type': join_type,
            'table': table,
            'ons': OnConditions(),
        })

    def on(self, *args, **kwds):
        if not self._joins:
            raise InvalidQueryException('You can not set join condition to nothing. Specify join table first.')
        self._joins[-1]['ons'].where(*args, **kwds)

    def _minimize_joins(self):
        """
        Minimizing of joins.
        Left/right and inner join of the same condition is only inner join.
        """
        joins_group = []
        for join in self._joins:
            append_new = True
            for join_group in joins_group:
                if join_group[0]['table'] == join['table'] and join_group[0]['ons'] == join['ons']:
                    join_group.append(join)
                    append_new = False
                    break
            if append_new:
                joins_group.append([join])

        self._joins = []
        for joins in joins_group:
            if len(joins) > 1 and any(bool(join['type'] == INNER_JOIN) for join in joins):
                joins[0]['type'] = INNER_JOIN
                self._joins.append(joins[0])
            elif len(joins) > 1 and all(join['type'] == joins[0]['type'] for join in joins):
                self._joins.append(joins[0])
            else:
                self._joins.extend(joins)


class Tables(QueryParts):
    def set(self, *args, **kwds):
        args = [arg for arg in args if arg]

        options = {
            'max_items': 2,
            'allow_dict': True,
        }
        for table_name, as_ in parse_args(options, *args, **kwds):
            self.append_unique_part(Table(table_name, as_))

        return self

    def is_simple(self):
        """Is set only one table without any join?"""
        return len(self._parts) == 1 and self._parts[0].is_simple()

    def join(self, arg):
        return self.inner_join(arg)

    def inner_join(self, arg):
        self.last_table().join(arg, INNER_JOIN)
        return self

    def left_join(self, arg):
        self.last_table().join(arg, LEFT_JOIN)
        return self

    def right_join(self, arg):
        self.last_table().join(arg, RIGHT_JOIN)
        return self

    def full_join(self, arg):
        backend = get_backend()
        if not backend.supports_full_join:
            raise InvalidQueryException('Backend {} does not support FULL JOIN.'.format(backend.name))
        self.last_table().join(arg, FULL_JOIN)
        return self

    def on(self, *args, **kwds):
        self.last_table().on(*args, **kwds)
        return self

    def last_table(self):
        if self._parts:
            return self._parts[-1]
        raise InvalidQueryException('You can not do join to nothing. Specify table first.')


class TablesForSelect(Tables):
    _keyword_of_parts = 'FROM'
