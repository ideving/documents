### 常用操作

#### 1.export one database
```cassandraql
mysqldump -u dbuser -p dbname > dbname.sql
```

#### 2.export one table
```cassandraql
mysqldump -u dbuser -p dbname tbname > dbname_tb.sql
```

#### 3.export one database or table structure
```cassandraql
mysqldump -u dbuser -p -d --add-drop-table dbname > dbname.database
mysqldump -u dbuser -p -d --add-drop-table dbname tbname > dbname_tb.database
-d no data
--add-drop-table  add drop table before create table
```

#### 4.export query
```cassandraql
mysql -u dbuser -p --default-character-set=gbk -e "select * from tbname" dbname > tbname.database
```

#### 5.import data
```cassandraql
mysql -u dbuser -p --default-character-set=gbk
mysql>show databases;
mysql>use dbname;
mysql>source dbname.sql;
```

#### 6.import one database or table
```cassandraql
mysql -u dbuser -p --default-character-set=gbk dbname < dbname.database
mysql -u dbuser -p --default-character-set=gbk dbname tbname < dbname_tb.database
```

#### 7.show database
```cassandraql
mysql -u dbuser -p --default-character-set=gbk
mysql>show databases;
mysql>use dbname;
mysql>show tables;
mysql>show columns from tbname;
```

### 重置密码

- view version
```
mysql --version
```

- edit /etc/my.cnf
```
# [mysqld] add content
skip-grant-tables
```

- restart mysql
```
service mysqld restart
```

- edit password for root
```
mysql
mysql> UPDATE mysql.user SET password = PASSWORD('toor') WHERE user = 'root';
mysql> flush privileges;
mysql> exit
```

- edit /etc/my.cnf
```
# [mysqld] remove content
skip-grant-tables
```

- restart mysql
```
service mysqld restart
```

- login mysql
```
mysql -uroot -p
```