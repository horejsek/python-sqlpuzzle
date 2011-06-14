### Python library for ease of writing SQL queries.

Examples:

    >>> import sqlPuzzle
    
    >>> print sqlPuzzle.selectFrom('table')
    SELECT * FROM `table`
    
    >>> print sqlPuzzle.select('id', ('user_name', 'userName')).from_('table')
    SELECT `id`, `user_name` AS "userName" FROM `table`
    
    >>> print sqlPuzzle.selectFrom('table').\
    ... where(name='Alan').\
    ... where('age', 20, sqlPuzzle.relations.LE).\
    ... where({'sex': 'male'}).\
    ... where(
    ...     ('column', 'value', sqlPuzzle.relations.LIKE),
    ...     ('id', range(5,15,2))
    ... )
    SELECT * FROM `table` WHERE `name` = "Alan" AND `age` <= 20 AND `sex` = "male" AND `column` LIKE "value" AND `id` IN (5, 7, 9, 11, 13)
    
    >>> print sqlPuzzle.selectFrom('table').limit(5, 20)
    SELECT * FROM `table` LIMIT 5 OFFSET 20
    
    >>> print sqlPuzzle.insertInto('table').values(name='Michael', age=20)
    INSERT INTO `table` (`age`, `name`) VALUES (20, "Michael")
    
    >>> print sqlPuzzle.update('table').set(name='Michale').where(id=42)
    UPDATE `table` SET `name` = "Michale" WHERE `id` = 42
    
    >>> print sqlPuzzle.update('table').set(name='Michale')
    Traceback (most recent call last):
      ...
    ConfirmUpdateAllException: Are you sure, that you want update all records?
    
    >>> print sqlPuzzle.deleteFrom('table').where(id=42)
    DELETE FROM `table` WHERE `id` = 42
    
    >>> print sqlPuzzle.deleteFrom('table')
    Traceback (most recent call last):
      ...
    ConfirmDeleteAllException: Are you sure, that you want delete all records?

Enjoy!
