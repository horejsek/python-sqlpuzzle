# -*- coding: utf-8 -*-
#
# sqlpuzzle
# Michal Horejsek <horejsekmichal@gmail.com>
# https://github.com/horejsek/sqlpuzzle
#

import sqlpuzzle.features.order


class GroupBy(sqlpuzzle.features.order.Orders):
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

