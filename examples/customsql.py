#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlpuzzle


avg = sqlpuzzle.customsql('AVG(`age`) AS "avgAge"')
table = sqlpuzzle.customsql('`user` LEFT JOIN `country` ON `user`.`country_id`=`country`.`id`')
where = sqlpuzzle.customsql('(`enable` = 1 OR `vip` = 1)')

sql = sqlpuzzle.select('country.name', avg).from_(table)
sql.where(where).where(planet='Earth')
sql.group_by('user.country_id')

print(sql)
#
# output:
# (for better reading splited to more lines)
#
# SELECT `country`.`name`, AVG(`age`) AS "avgAge"
# FROM `user` LEFT JOIN `country` ON `user`.`country_id`=`country`.`id`
# WHERE (`enable` = 1 OR `vip` = 1) AND `planet` = 'Earth'
# GROUP BY `user`.`country_id`
#


table = sqlpuzzle.customsql('`user`')
set_ = sqlpuzzle.customsql('`age` = `age` + 1')

sql = sqlpuzzle.update(table).set(set_).where(where)
print(sql)
# output:
# UPDATE `user` SET `age` = `age` + 1 WHERE (`enable` = 1 OR `vip` = 1)


print(sqlpuzzle.delete_from(table).where(where))
# output:
# DELETE FROM `user` WHERE (`enable` = 1 OR `vip` = 1)


print(sqlpuzzle.insert_into(table).values(name='Alan'))
# output:
# INSERT INTO `user` (`name`) VALUES ("Alan")
