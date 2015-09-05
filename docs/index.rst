SQLPuzzle documentation
#######################

.. automodule:: sqlpuzzle

Installation
************

.. code-block:: bash

    pip install sqlpuzzle

Documentation
*************

Note there are also `camelCase` methods which are only aliases to methods described
here. It's only for backward compatiblity with version 0.x. It will be removed one day.

Configuration
=============

.. autofunction:: sqlpuzzle.configure

Base methods
============

.. automodule:: sqlpuzzle
    :members:
        select,
        select_from,
        insert,
        insert_into,
        update,
        delete,
        delete_from

Helpers
=======

.. automodule:: sqlpuzzle
    :members:
        Q,
        C,
        V,
        R

Functions
=========

.. automodule:: sqlpuzzle
    :members:
        avg,
        avg_distinct,
        count,
        count_distinct,
        max,
        max_distinct,
        min,
        min_distinct,
        sum,
        sum_distinct,
        concat,
        group_concat,
        convert

.. autoclass:: sqlpuzzle._queryparts.functions.GroupConcat
    :members:

.. autoclass:: sqlpuzzle._queryparts.functions.Convert
    :members:

Relations
=========

.. automodule:: sqlpuzzle.relations
    :members:

Select
======

.. autoclass:: sqlpuzzle._queries.select.Select
    :members:

Insert
======

.. autoclass:: sqlpuzzle._queries.insert.Insert
    :members:

Update
======

.. autoclass:: sqlpuzzle._queries.update.Update
    :members:

Delete
======

.. autoclass:: sqlpuzzle._queries.delete.Delete
    :members:

Exceptions
==========

.. automodule:: sqlpuzzle.exceptions
    :members:
