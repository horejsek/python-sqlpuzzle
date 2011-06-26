# -*- coding: utf-8 -*-
#
# SqlPuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlPuzzle
#

import sqlPuzzle.features.order


class GroupBy(sqlPuzzle.features.order.Orders):
    def __str__(self):
        """Print order (part of query)."""
        groupBy = "GROUP BY %s" % ', '.join(str(order) for order in self._orders)
        return groupBy
    
    def __repr__(self):
        return "<GroupBy: %s>" % self.__str__()
    
    def groupBy(self, *args):
        """Set GROUP BY."""
        self.order(*args)
        return self

