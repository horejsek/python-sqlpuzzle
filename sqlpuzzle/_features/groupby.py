# -*- coding: utf-8 -*-

import sqlpuzzle._features.order


class GroupBy(sqlpuzzle._features.order.Orders):
    def __init__(self):
        """Initialization of GroupBy."""
        super(GroupBy, self).__init__()
        self._keyword_of_feature = 'GROUP BY'

    def group_by(self, *args, **kwds):
        """Set GROUP BY."""
        self.order(*args, **kwds)
        return self
