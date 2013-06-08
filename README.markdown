# sqlpuzzle

Python library for ease of writing SQL queries. For now only for database MySQL.

## Requirements

- Python 2.5 or later.

## Installation

Installation of Python module `sqlpuzzle` is very simple - just extract archive
and then from created directory sqlpuzzle run this command:

    $ sudo make install

That's all! After this step you can start your favorite Python interpret (perhaps
bpython) and try import module `sqlpuzzle`. See for examples below.


## Examples:

    >>> import sqlPuzzle

    >>> print sqlPuzzle.select_from('table')
    SELECT * FROM `table`

    >>> print sqlPuzzle.select('id', ('user_name', 'userName')).from_('table')
    SELECT `id`, `user_name` AS "userName" FROM `table`

    >>> print sqlPuzzle.select_from('table').\
    ... where(name='Alan').\
    ... where('age', sqlPuzzle.relations.LE(20)).\
    ... where({'sex': 'male'}).\
    ... where(
    ...     ('column', sqlPuzzle.relations.LIKE('value')),
    ...     ('id', range(5,15,2))
    ... )
    SELECT * FROM `table` WHERE `name` = "Alan" AND `age` <= 20 AND `sex` = "male" AND `column` LIKE "value" AND `id` IN (5, 7, 9, 11, 13)

    >>> print sqlPuzzle.select_from('table').limit(5, 20)
    SELECT * FROM `table` LIMIT 5 OFFSET 20

    >>> print sqlPuzzle.insert_into('table').values(name='Michael', age=20)
    INSERT INTO `table` (`age`, `name`) VALUES (20, "Michael")

    >>> print sqlPuzzle.update('table').set(name='Michale').where(id=42)
    UPDATE `table` SET `name` = "Michale" WHERE `id` = 42

    >>> print sqlPuzzle.update('table').set(name='Michale')
    Traceback (most recent call last):
      ...
    ConfirmUpdateAllException: Are you sure, that you want update all records?

    >>> print sqlPuzzle.delete_from('table').where(id=42)
    DELETE FROM `table` WHERE `id` = 42

    >>> print sqlPuzzle.delete_from('table')
    Traceback (most recent call last):
      ...
    ConfirmDeleteAllException: Are you sure, that you want delete all records?

Enjoy!
