# elasticsearch

- create network
```
docker network create elk
```

- run elasticsearch 
```
docker run --name elasticsearch -d --net elk -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elastic/elasticsearch:7.0.0
```

# logstash

- run logstash
```
docker run --name logstash -dit --net elk --link elasticsearch:elasticsearch -p 5044:5044 -p 9600:9600 -v ~/logstash/config:/usr/share/logstash/config -v ~/logs:/var/logs elastic/logstash:7.0.0
# or
docker run --name logstash -dit --net elk --link elasticsearch:elasticsearch -p 5044:5044 -p 9600:9600 -v ~/logstash/config:/usr/share/logstash/config -v ~/logs:/var/logs elastic/logstash:7.0.0 logstash -f /usr/share/logstash/config/logstash-sample.conf
```
- config dir content
> cd ~/logstash/config
> vi logstash.yml
```
# none
```
> vi pipelines.yml
```
- pipeline.id: logstash-one
  path.config: "/usr/share/logstash/config/*.conf"
  pipeline.workers: 3
```

> vi logstash-sample.conf
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

# kibana

- run kibana

```
docker run --name kibana -dit --net elk --link elasticsearch:elasticsearch -p 5601:5601 elastic/kibana:7.0.0
```
