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
mysqldump -u dbuser -p -d --add-drop-table dbname > dbname.sql
mysqldump -u dbuser -p -d --add-drop-table dbname tbname > dbname_tb.sql
-d no data
--add-drop-table  add drop table before create table
```

#### 4.export query
```cassandraql
mysql -u dbuser -p --default-character-set=gbk -e "select * from tbname" dbname > tbname.sql
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
mysql -u dbuser -p --default-character-set=gbk dbname < dbname.sql
mysql -u dbuser -p --default-character-set=gbk dbname tbname < dbname_tb.sql
```

#### 7.show database
```cassandraql
mysql -u dbuser -p --default-character-set=gbk
mysql>show databases;
mysql>use dbname;
mysql>show tables;
mysql>show columns from tbname;
```
