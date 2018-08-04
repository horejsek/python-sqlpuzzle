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

To all methods you can pass arguments of different types. I know, in ``this`` is
line saying *There should be one-- and preferably only one --obvious way to do it.*
but you can have different type of data for different type of SQL and why to
support only one style and force user to deal with it everywhere.

So you should note that you can:

 1. Pass single argument. For example for table, column, …

 .. code-block:: python

    >>> sqlpuzzle.select('column').from_('table')
    <Select: SELECT "column" FROM "table">

 2. Pass several arguments. Where you can pass only one argument, most of there
    time you can also pass several arguments.

 .. code-block:: python

    >>> sqlpuzzle.select('c1', 'c2').from_('t1', 't2')
    <Select: SELECT "c1", "c2" FROM "t1", "t2">

 3. Pass ``tuple`` or ``list``. Because you want for example make aliases.
    Advantage of ``tuple`` is that you can pass it only when you need alias.

 .. code-block:: python

    >>> sqlpuzzle.select('c1', 'c2').from_('t', ('t', 't2'))
    <Select: SELECT "c1", "c2" FROM "t", "t" AS "t2">

 4. Pass ``dict``. Because it's more sexy than tuples. Usage is same. You just
    have to be aware that ``dict`` is not sorted, so if you need same order,
    use ``OrderedDict`` instead. And also with same key you can have only one
    value.

 .. code-block:: python

    >>> sqlpuzzle.select('c').from_('t').where({'x': 1, 'y': 2})
    <Select: SELECT "c" FROM "t" WHERE "x" = 1 AND "y" = 2>

 5. Pass named arugments. Which is same as ``dict`` above.

 .. code-block:: python

    >>> sqlpuzzle.select('c').from_('t').where(x=1, y=2)
    <Select: SELECT "c" FROM "t" WHERE "x" = 1 AND "y" = 2>

Configuration
=============

.. autofunction:: sqlpuzzle.configure

Base methods
============

.. autofunction:: sqlpuzzle.select
.. autofunction:: sqlpuzzle.select_from
.. autofunction:: sqlpuzzle.insert
.. autofunction:: sqlpuzzle.insert_into
.. autofunction:: sqlpuzzle.update
.. autofunction:: sqlpuzzle.delete
.. autofunction:: sqlpuzzle.delete_from

Helpers
=======

.. autofunction:: sqlpuzzle.Q
.. autofunction:: sqlpuzzle.C
.. autofunction:: sqlpuzzle.V
.. autofunction:: sqlpuzzle.R

Functions
=========

.. autofunction:: sqlpuzzle.exists
.. autofunction:: sqlpuzzle.avg
.. autofunction:: sqlpuzzle.avg_distinct
.. autofunction:: sqlpuzzle.count
.. autofunction:: sqlpuzzle.count_distinct
.. autofunction:: sqlpuzzle.max
.. autofunction:: sqlpuzzle.max_distinct
.. autofunction:: sqlpuzzle.min
.. autofunction:: sqlpuzzle.min_distinct
.. autofunction:: sqlpuzzle.sum
.. autofunction:: sqlpuzzle.sum_distinct
.. autofunction:: sqlpuzzle.concat
.. autofunction:: sqlpuzzle.group_concat
.. autofunction:: sqlpuzzle.convert

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
    :undoc-members:
    :members:
        has,
        __and__,
        __or__,
        columns,
        from_,
        from_table,
        from_tables,
        join,
        inner_join,
        left_join,
        right_join,
        full_join,
        on,
        where,
        having,
        group_by,
        order_by,
        limit,
        offset,
        into_outfile,
        fields_terminated_by,
        lines_terminated_by,
        optionally_enclosed_by,
        sql_cache,
        sql_no_cache,
        all,
        distinct,
        distinctrow,
        sql_small_result,
        sql_big_result,
        sql_buffer_result,
        sql_calc_found_rows,
        straight_join,
        high_priority,
        for_update

Union
=====

.. autoclass:: sqlpuzzle._queries.union.Union
    :undoc-members:
    :members:
        __and__,
        __or__

Insert
======

.. autoclass:: sqlpuzzle._queries.insert.Insert
    :undoc-members:
    :members:
        into,
        values,
        on_duplicate_key_update,
        ignore

Update
======

.. autoclass:: sqlpuzzle._queries.update.Update
    :undoc-members:
    :members:
        allow_update_all,
        forbid_update_all,
        table,
        set,
        where,
        join,
        inner_join,
        left_join,
        right_join,
        on,
        ignore

Delete
======

.. autoclass:: sqlpuzzle._queries.delete.Delete
    :undoc-members:
    :members:
        allow_delete_all,
        forbid_delete_all,
        delete,
        from_,
        from_table,
        from_tables,
        join,
        inner_join,
        left_join,
        right_join,
        on,
        where,
        ignore

Exceptions
==========

.. automodule:: sqlpuzzle.exceptions
    :members:
