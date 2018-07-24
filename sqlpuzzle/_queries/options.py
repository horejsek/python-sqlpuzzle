from sqlpuzzle._common import Object, force_text
from sqlpuzzle._queryparts.queryparts import has

__all__ = ()


class Options(Object):
    _definition_of_options = {}

    def __init__(self):
        super().__init__()
        self._options = {}
        for option_key in self._definition_of_options:
            self._options[option_key] = 'off'

    def __str__(self):
        return ' '.join(sorted(
            self._definition_of_options[key][val]
            for key, val in self._options.items()
            if val != 'off'
        ))

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and len(self._options) == len(other._options)
            and all(bool(so == oo) for so, oo in zip(self._options.values(), other._options.values()))
        )

    def has(self, value):
        return has(self, force_text(value).upper())

    @property
    def is_set(self):
        return any(item != 'off' for item in self._options.values())
