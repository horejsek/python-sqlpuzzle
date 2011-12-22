# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle._features.order


class GroupBy(sqlpuzzle._features.order.Orders):
    def __init__(self):
        """Initialization of GroupBy."""
        super(GroupBy, self).__init__()
        self._keywordOfFeature = 'GROUP BY'

    def groupBy(self, *args, **kwds):
        """Set GROUP BY."""
        self.order(*args, **kwds)
        return self
