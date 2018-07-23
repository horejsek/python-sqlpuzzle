from sqlpuzzle._common import Object
from sqlpuzzle._queries.options import Options

__all__ = ()


class SelectOptions(Options):
    _definition_of_options = {
        'sql_cache': {
            'off': '',
            'cache': 'SQL_CACHE',
            'no_cache': 'SQL_NO_CACHE'
        },
        'duplicated': {
            'off': '',
            'all': 'ALL',
            'distinct': 'DISTINCT',
            'distinctrow': 'DISTINCTROW',
        },
        'sql_small_result': {
            'off': '',
            'on': 'SQL_SMALL_RESULT',
        },
        'sql_big_result': {
            'off': '',
            'on': 'SQL_BIG_RESULT',
        },
        'sql_buffer_result': {
            'off': '',
            'on': 'SQL_BUFFER_RESULT',
        },
        'sql_calc_found_rows': {
            'off': '',
            'on': 'SQL_CALC_FOUND_ROWS',
        },
        'straight_join': {
            'off': '',
            'on': 'STRAIGHT_JOIN',
        },
        'high_priority': {
            'off': '',
            'on': 'HIGH_PRIORITY',
        },
    }

    def sql_cache(self, allow=True):
        self._options['sql_cache'] = 'cache' if allow else 'off'

    def sql_no_cache(self, allow=True):
        self._options['sql_cache'] = 'no_cache' if allow else 'off'

    def all(self, allow=True):
        self._options['duplicated'] = 'all' if allow else 'off'

    def distinct(self, allow=True):
        self._options['duplicated'] = 'distinct' if allow else 'off'

    def distinctrow(self, allow=True):
        self._options['duplicated'] = 'distinctrow' if allow else 'off'

    def sql_small_result(self, allow=True):
        self._options['sql_small_result'] = 'on' if allow else 'off'

    def sql_big_result(self, allow=True):
        self._options['sql_big_result'] = 'on' if allow else 'off'

    def sql_buffer_result(self, allow=True):
        self._options['sql_buffer_result'] = 'on' if allow else 'off'

    def sql_calc_found_rows(self, allow=True):
        self._options['sql_calc_found_rows'] = 'on' if allow else 'off'

    def straight_join(self, allow=True):
        self._options['straight_join'] = 'on' if allow else 'off'

    def high_priority(self, allow=True):
        self._options['high_priority'] = 'on' if allow else 'off'


class SelectForUpdate(Object):
    def __init__(self):
        super(SelectForUpdate, self).__init__()
        self._for_update = False

    def __unicode__(self):
        if self._for_update:
            return 'FOR UPDATE'
        return ''

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self._for_update == other._for_update
        )

    @property
    def is_set(self):
        return self._for_update

    def has(self, value):
        return has(self, value)

    def for_update(self, allow=True):
        self._for_update = bool(allow)
