### docker mysql

#### 1.pull mysql
```cassandraql
docker pull mysql
```

#### 2.docker run
```cassandraql
docker tag mysql:5.5 mysql:v1.0.0
docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 --name mysql mysql:v1.0.0
docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --name mysql mysql:v1.0.0
```

#### 3.set host
```cassandraql
mysql -u dbuser -p --default-character-set=gbk
mysql>use mysql; 
mysql>update user set host = '%' where user = 'root'; 
```

#### 4.grant privileges
```cassandraql
mysql>grant all privileges on *.* to 'root'@'%' identified by 'toor' with grant option;
```

#### 5.docker run best
> 5.1 make dir
```cassandraql
cd /home
mkdir mysql
cd mysql
mkdir conf
mkdir data
cd conf
```

> 5.2 vi mysql.conf
```cassandraql
#/home/mysql/conf/mysql.conf

[client]
default-character-set=utf8
 
[mysql]
default-character-set=utf8
 
[mysqld]
init_connect='SET collation_connection = utf8_unicode_ci'
init_connect='SET NAMES utf8'
character-set-server=utf8
collation-server=utf8_unicode_ci
skip-character-set-client-handshake
```

> 5.3 docker run
```cassandraql
docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 --restart=always --privileged=true -v /home/mysql/conf/mysql.conf:/etc/mysql/my.cnf -v /home/mysql/data:/var/lib/mysql --name mysql mysql:v1.0.0
```

#### 6.docker command
```cassandraql
docker xxx --help
docker images
docker ps -a
docker inspect id
docker tag sourec:tag target:tag
docker build -t repository:tag -f Dockerfile .  
docker save -o one.tar image
docker load -i one.tar
docker export -o one.tar id
docker import one.tar repository:tag
docker logs id
docker start id
docker restart id
docker stop id
docker run -d -it --name cname image
docker exec -it -u root id bash
docker rmi image -f
docker rm id -f
```