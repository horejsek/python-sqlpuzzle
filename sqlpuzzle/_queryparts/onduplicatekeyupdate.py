from .values import Values

__all__ = ('OnDuplicateKeyUpdate',)


class OnDuplicateKeyUpdate(Values):
    _keyword_of_parts = 'ON DUPLICATE KEY UPDATE'
