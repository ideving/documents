# 一、前言
## 1. ELK简介
ELK是Elasticsearch+Logstash+Kibana的简称

- ElasticSearch是一个基于Lucene的分布式全文搜索引擎，提供 RESTful API进行数据读写

- Logstash是一个收集，处理和转发事件和日志消息的工具

- Kibana是Elasticsearch的开源数据可视化插件，为查看存储在ElasticSearch提供了友好的Web界面，并提供了条形图，线条和散点图，饼图和地图等分析工具

总的来说，ElasticSearch负责存储数据，Logstash负责收集日志，并将日志格式化后写入ElasticSearch，Kibana提供可视化访问ElasticSearch数据的功能。

## 2、ELK工作流

ELK工作流

应用将日志按照约定的Key写入Redis，Logstash从Redis中读取日志信息写入ElasticSearch集群。Kibana读取ElasticSearch中的日志，并在Web页面中以表格/图表的形式展示。

# 二、准备工作
## 1、服务器&软件环境说明
- 服务器

一共准备3台CentOS7 Server

es1	192.168.1.31	部署ElasticSearch主节点

es2	192.168.1.32	部署ElasticSearch从节点

elk	192.168.1.21	部署Logstash + Kibana + Redis

这里为了节省，只部署2台Elasticsearch，并将Logstash + Kibana + Redis部署在了一台机器上。
如果在生产环境部署，可以按照自己的需求调整。

- 软件环境

Linux Server	CentOS 7

Elasticsearch	6.0.0

Logstash	6.0.0

Kibana	6.0.0

Redis	4.0

JDK	1.8

## 2、ELK环境准备

由于Elasticsearch、Logstash、Kibana均不能以root账号运行。
但是Linux对非root账号可并发操作的文件、线程都有限制。
所以，部署ELK相关的机器都要调整：

- 修改文件限制
```
# 修改系统文件
vi /etc/security/limits.conf

#增加的内容

* soft nofile 65536
* hard nofile 65536
* soft nproc 2048
* hard nproc 4096
```

- 调整进程数
```
#修改系统文件
vi /etc/security/limits.d/20-nproc.conf
 
#调整成以下配置
*          soft    nproc     4096
root       soft    nproc     unlimited
```

- 调整虚拟内存&最大并发连接
```
#修改系统文件
vi /etc/sysctl.conf
 
#增加的内容
vm.max_map_count=655360
fs.file-max=655360
```
以上操作重启系统后生效

- JDK安装
```
rpm -iv jdk.rpm
```

- 创建专用用户
```
useradd elk
```

- 创建相关目录并赋权
```
#创建应用目录
mkdir /opt/elk
#创建数据目录
mkdir /elk
 
#更改目录拥有者
chown -R elk:elk /opt/elk
chown -R elk:elk /elk
```

- 下载包并解压
```
#打开文件夹
cd /home/download
 
#下载
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.0.0.tar.gz
wget https://artifacts.elastic.co/downloads/logstash/logstash-6.0.0.tar.gz
wget https://artifacts.elastic.co/downloads/kibana/kibana-6.0.0.tar.gz
 
#解压
tar -zvxf elasticsearch-6.0.0.tar.gz
tar -zvxf logstash-6.0.0.tar.gz
tar -zvxf kibana-6.0.0.tar.gz
```

# 三、Elasticsearch 部署
本次一共要部署两个Elasticsearch节点，所有文中没有指定机器的操作都表示每个Elasticsearch机器都要执行该操作

## 1、准备工作

- 移动Elasticsearch到统一目录
```
#移动目录
mv /home/download/elasticsearch-6.0.0 /opt/elk
#赋权
chown -R elk:elk /opt/elk/elasticsearch-6.0.0
```

- 开放端口
```
#增加端口
firewall-cmd --add-port=9200/tcp --permanent
firewall-cmd --add-port=9300/tcp --permanent
 
#重新加载防火墙规则
firewall-cmd --reload
```

-切换账号
```
su - elk
```

- 数据&日志目录
```
创建Elasticsearch主目录
mkdir /elk/es
#创建Elasticsearch数据目录
mkdir /elk/es/data
#创建Elasticsearch日志目录
mkdir /elk/es/logs
```

## 2、Elasticsearch节点配置

- 修改配置
```
#打开目录
cd /opt/elk/elasticsearch-6.0.0
 
#修改配置
 
vi config/elasticsearch.yml
```

- 主节点配置（192.168.1.31）
```
cluster.name: es 
node.name: es1
path.data: /elk/es/data
path.logs: /elk/es/logs
network.host: 192.168.1.31
http.port: 9200
transport.tcp.port: 9300
node.master: true
node.data: true
discovery.zen.ping.unicast.hosts: ["192.168.1.31:9300","192.168.1.32:9300"]
discovery.zen.minimum_master_nodes: 1
```

- 从节点配置（192.168.1.32）
```
cluster.name: es 
node.name: es2
path.data: /elk/es/data
path.logs: /elk/es/logs
network.host: 192.168.1.32
http.port: 9200
transport.tcp.port: 9300
node.master: false
node.data: true
discovery.zen.ping.unicast.hosts: ["192.168.1.31:9300","192.168.1.32:9300"]
discovery.zen.minimum_master_nodes: 1
```

- 配置项说明
```
配置    说明
cluster.name	集群名
node.name	节点名
path.data	数据保存目录
path.logs	日志保存目录
network.host	节点host/ip
http.port	HTTP访问端口
transport.tcp.port	TCP传输端口
node.master	是否允许作为主节点
node.data	是否保存数据
discovery.zen.ping.unicast.hosts	集群中的主节点的初始列表,当节点(主节点或者数据节点)启动时使用这个列表进行探测
discovery.zen.minimum_master_nodes	主节点个数
```

## 3、Elasticsearch启动&健康检查
- 启动
```
#进入elasticsearch根目录
cd /opt/elk/elasticsearch-6.0.0
#启动
./bin/elasticsearch
```

- 查看健康状态
```
curl http://192.168.1.31:9200/_cluster/health
```
如果返回status=green表示正常
```
{
  "cluster_name": "esc",
  "status": "green",
  "timed_out": false,
  "number_of_nodes": 2,
  "number_of_data_nodes": 2,
  "active_primary_shards": 0,
  "active_shards": 0,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 0,
  "delayed_unassigned_shards": 0,
  "number_of_pending_tasks": 0,
  "number_of_in_flight_fetch": 0,
  "task_max_waiting_in_queue_millis": 0,
  "active_shards_percent_as_number": 100.0
}
```

# 四、Logstash 部署
## 1、准备工作
- 部署Redis(略)

- 移动Logstash到统一目录
```
#移动目录
mv /home/download/logstash-6.0.0 /opt/elk
#赋权
chown -R elk:elk /opt/elk/logstash-6.0.0
```

- 切换账号
```
#账号切换到 elk
su - elk
```

- 数据&日志目录
```
#创建Logstash主目录
mkdir /elk/logstash
#创建Logstash数据目录
mkdir /elk/logstash/data
#创建Logstash日志目录
mkdir /elk/logstash/logs
```

## 2、Logstash配置
- 配置数据&日志目录
```
#打开目录
cd /opt/elk/logstash-6.0.0
#修改配置
vi config/logstash.yml
 
#增加以下内容
path.data: /elk/logstash/data
path.logs: /elk/logstash/logs
```

- 配置Redis&Elasticsearch
```
vi config/input-output.conf
 
#配置内容
 
input {
  redis {
    data_type => "list"
    key => "logstash"
    host => "192.168.1.21"
    port => 6379
    threads => 5
    codec => "json"
  }
}
filter {
}
output {
  elasticsearch {
    hosts => ["192.168.1.31:9200","192.168.1.32:9200"]
    index => "logstash-%{type}-%{+YYYY.MM.dd}"
    document_type => "%{type}"
  }
  stdout {
  }
}
```
该配置就是从redis中读取数据，然后写入指定的elasticsearch。
Redis核心配置项说明：
```
配置项	说明
data_type => "list"	数据类型为list
key => "logstash"	缓存key为：logstash
codec => "json"	数据格式为：json
```

- 启动
```
#进入Logstash根目录
cd /opt/elk/logstash-6.0.0
#测试
./bin/logstash -t -f config/input-output.conf
#启动
./bin/logstash -f config/input-output.conf
```
启动成功后，在启动输出的最后一行会看到如下信息：
```
[INFO ][logstash.pipeline        ] Pipeline started {"pipeline.id"=>"main"}
[INFO ][logstash.agent           ] Pipelines running {:count=>1, :pipelines=>["main"]}
```

# 五、Kibana 部署
## 1、准备工作
- 移动Kibana到统一目录
```
#移动目录
mv /home/download/kibana-6.0.0-linux-x86_64 /opt/elk/kibana-6.0.0
#赋权
chown -R elk:elk /usr/elk/kibana-6.0.0
```

- 开放端口
```
#增加端口
firewall-cmd --add-port=5601/tcp --permanent
 
#重新加载防火墙规则
firewall-cmd --reload
```

- 切换账号
```
#账号切换到 elk
su - elk
```

## 3、Kibana配置与访问测试
- 修改配置
```
#进入kibana-6.0.0根目录
cd /opt/elk/kibana-6.0.0
#修改配置
vi config/kibana.yml
 
#增加以下内容
server.port: 5601
server.host: "192.168.1.21"
elasticsearch.url: "http://192.168.1.31:9200" 
```
- 启动
```
#进入kibana-6.0.0根目录
cd /opt/elk/kibana-6.0.0
#启动
./bin/kibana
```

- 访问

http://192.168.1.21:5601

# 六、测试
## 1、日志写入
日历写入的话，写入到logstash监听的redis即可。
数据类型之前在/opt/elk/logstash-6.0.0/config/input-uput.conf中有配置

- Redis命令方式
```
#启动redis客户端
#执行以下命令
lpush logstash '{"host":"127.0.0.1","type":"logtest","message":"hello"}'
```
- Java代码批量写入（引入Jedis）
```
Jedis jedis = new Jedis("192.168.1.21", 6379);
for (int i = 0; i < 1000; i++) {
    jedis.lpush("logstash", "{\"host\":\"127.0.0.1\",\"type\":\"logtest\",\"message\":\"" + i + "\"}");
}
```

## 2、Kibana使用
```
http://192.168.1.21:5601/app/kibana#/discover
```

# Other
## Logstash配置
- config.conf
```
input{
    file{
        path => ["/logs/out.log","/logs/error.log"]
        start_position => "beginning"
        type => "logstash_log"
    }
}
filter{
}
output{
    elasticsearch{
        hosts => ["192.168.1.31:9200","192.168.1.32:9200"]
        index => "logstash-%{type}-%{+YYYY.MM.dd}"
        document_type => "%{type}"
    }
    stdout{
    }
}
```
