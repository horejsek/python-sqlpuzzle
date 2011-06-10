### Python library for ease of writing SQL queries.

Example:

    import sqlPuzzle
    
    print sqlPuzzle.select().from_('table')
    // output: "SELECT * FROM `table`"
    
    print sqlPuzzle.select('id', ('user_name', 'userName')).from_('table')
    // output: "SELECT `id`, `user_name` AS "userName" FROM `table`"
    
    print sqlPuzzle.select().from_('t').where(name='Alan')
    // output: "SELECT * FROM `t` WHERE `name` = "Alan""
    
    print sqlPuzzle.select().from_('t').where('age', 20, sqlPuzzle.relations.LE)
    // output: "SELECT * FROM `t` WHERE `age` <= 20"
    
    print sqlPuzzle.select().from_('t').limit(5).offset(20)
    // output: "SELECT * FROM `t` LIMIT 5 OFFSET 20"
    
    print sqlPuzzle.insert().into('table').values(name='Harry')
    // output: "INSERT INTO `table` (`name`) VALUES ("Harry")"
    
    print sqlPuzzle.update('table').set(name='Alan').where(name='Harry')
    // output: "UPDATE `table` SET `name` = "Alan" WHERE `name` = "Harry""
    
    print sqlPuzzle.delete().from_('table')
    // throw ConfirmDeleteAllException
    
    print sqlPuzzle.delete().from_('table').allowDeleteAll()
    // output: "DELETE FROM `table`"

Enjoy!
