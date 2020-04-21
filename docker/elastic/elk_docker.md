# 1. elasticsearch

- create network
```
docker network create elk
```

- run elasticsearch 
```
docker run --name elasticsearch -d --net elk -p 9200:9200 -p 9300:9300 \
-e "discovery.type=single-node" elastic/elasticsearch:7.0.0
```

# 2. logstash

- run logstash use config file
```
docker run --name logstash -dit --net elk --link elasticsearch:elasticsearch \
-p 5044:5044 -p 9600:9600 -v ~/logstash:/mnt logstash -f /mnt/logstash-sample.conf
```

- logstash dir content
- cd ~/logstash
- vi logstash-sample.conf
    
```
input {
    file {
        path => "/mnt/logs/sys*.log"
        type => "system"
        start_position => "beginning"
    }
    file {
        path => "/mnt/logs/error*.log"
        type => "error"
        start_position => "beginning"
    }
}
output {
    if [type] == "system" {
        elasticsearch {
            hosts => ["http://elasticsearch:9200"]
            index => "system-%{+YYYY.MM.dd}"
        }
    }
    if [type] == "error" {
        elasticsearch {
            hosts => ["http://elasticsearch:9200"]
            index => "error-%{+YYYY.MM.dd}"
        }
    }
}
```

- run logstash
```
docker run --name logstash -dit --net elk --link elasticsearch:elasticsearch \
-p 5044:5044 -p 9600:9600 -v ~/logstash/config:/usr/share/logstash/config \
-v ~/logs:/var/logs elastic/logstash:7.0.0
```

- config dir content
- cd ~/logstash/config
- vi logstash.yml
```
# none
```

- vi pipelines.yml
```
- pipeline.id: logstash-one
  path.config: "/usr/share/logstash/config/*.conf"
  pipeline.workers: 3
```

- vi logstash-sample.conf
```
input {
    file {
        path => "/var/logs/sys*.log"
        type => "system"
        start_position => "beginning"
    }
    file {
        path => "/var/logs/error*.log"
        type => "error"
        start_position => "beginning"
    }
}
output {
    if [type] == "system" {
        elasticsearch {
            hosts => ["http://elasticsearch:9200"]
            index => "system-%{+YYYY.MM.dd}"
        }
    }
    if [type] == "error" {
        elasticsearch {
            hosts => ["http://elasticsearch:9200"]
            index => "error-%{+YYYY.MM.dd}"
        }
    }
}
```

# 3. kibana

- run kibana
```
docker run --name kibana -dit --net elk --link elasticsearch:elasticsearch \
-p 5601:5601 elastic/kibana:7.0.0
```

# 4. fast setup

## 4.1 load docker image
```
docker load -i elasticsearch.tar
docker load -i logstash.tar
docker load -i kibana.tar
```

## 4.2 edit logstash-sample.conf

- vi ~/logstash/logstash-sample.conf
```
input {
    file {
        path => "/mnt/logs/sys*.log"
        type => "system"
        start_position => "beginning"
    }
    file {
        path => "/mnt/logs/error*.log"
        type => "error"
        start_position => "beginning"
    }
}
output {
    if [type] == "system" {
        elasticsearch {
            hosts => ["http://elasticsearch:9200"]
            index => "system-%{+YYYY.MM.dd}"
        }
    }
    if [type] == "error" {
        elasticsearch {
            hosts => ["http://elasticsearch:9200"]
            index => "error-%{+YYYY.MM.dd}"
        }
    }
}
```

## 4.3 run docker
```
docker network create elk
docker run --name elasticsearch -d --net elk -p 9200:9200 -p 9300:9300 \
-e "discovery.type=single-node" elastic/elasticsearch:7.0.0

docker run --name kibana -dit --net elk --link elasticsearch:elasticsearch \
-p 5601:5601 elastic/kibana:7.0.0

docker run --name logstash -dit --net elk --link elasticsearch:elasticsearch \
-p 5044:5044 -p 9600:9600 -v ~/logstash:/mnt elastic/logstash:7.0.0 logstash -f /mnt/logstash-sample.conf
```

## 4.4 nginx config
```
server {
    listen 80;
    server_name www.example.com;
    proxy_set_header X-Forwarded-For $remote_addr;

    location / {
        proxy_pass http://localhost:5601;
    }
    location /kibana {
        proxy_pass http://localhost:5601;
        rewrite ^/kibana/(.*)$ /$1 break;
    }
}
```