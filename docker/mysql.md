### docker mysql

#### pull mysql
```cassandraql
docker pull mysql
```

#### docker run
```cassandraql
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=toor -d mysql:tag
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=toor -d mysql:tag --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

#### set host
```cassandraql
mysql>use mysql; 
mysql>update user set host = '%' where user = 'root'; 
```

#### grant privileges
```cassandraql
grant all privileges on *.* to 'root'@'%' identified by 'toor' with grant option;
```