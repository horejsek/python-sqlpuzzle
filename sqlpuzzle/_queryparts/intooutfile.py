from sqlpuzzle._common import SqlValue, check_type_decorator
from .queryparts import QueryPart

__all__ = ('IntoOutfile',)


class IntoOutfile(QueryPart):
    def __init__(
            self,
            into_outfile=None,
            fields_terminated_by=None,
            lines_terminated_by=None,
            optionally_enclosed_by=None,
    ):
        self._into_outfile = into_outfile
        self._fields_terminated_by = fields_terminated_by
        self._lines_terminated_by = lines_terminated_by
        self._optionally_enclosed_by = optionally_enclosed_by

    def __unicode__(self):
        into_outfile = 'INTO OUTFILE {}'.format(SqlValue(self._into_outfile))
        if self._fields_terminated_by is not None:
            into_outfile += ' FIELDS TERMINATED BY {}'.format(SqlValue(self._fields_terminated_by))
        if self._lines_terminated_by is not None:
            into_outfile += ' LINES TERMINATED BY {}'.format(SqlValue(self._lines_terminated_by))
        if self._optionally_enclosed_by is not None:
            into_outfile += ' OPTIONALLY ENCLOSED BY {}'.format(SqlValue(self._optionally_enclosed_by))
        return into_outfile

    def __eq__(self, other):
        return (
            type(self) == type(other) and
            self._into_outfile == other._into_outfile and
            self._fields_terminated_by == other._fields_terminated_by and
            self._lines_terminated_by == other._lines_terminated_by and
            self._optionally_enclosed_by == other._optionally_enclosed_by
        )

    @property
    def is_set(self):
        return self._into_outfile is not None

    @check_type_decorator(str)
    def into_outfile(self, into_outfile):
        self._into_outfile = into_outfile
        return self

    @check_type_decorator(str)
    def fields_terminated_by(self, fields_terminated_by):
        self._fields_terminated_by = fields_terminated_by
        return self

    @check_type_decorator(str)
    def lines_terminated_by(self, lines_terminated_by):
        self._lines_terminated_by = lines_terminated_by
        return self

    @check_type_decorator(str)
    def optionally_enclosed_by(self, optionally_enclosed_by):
        self._optionally_enclosed_by = optionally_enclosed_by
        return self
