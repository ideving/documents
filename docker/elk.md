# docker elk

## elasticsearch

- Copy and paste to pull this image

```
docker pull elasticsearch:7.0.0
```

- Running in Development Mode

Create user defined network (useful for connecting to other services attached to the same network (e.g. Kibana)):

```
docker network create somenetwork
```

Run Elasticsearch:

```
docker run -d --name elasticsearch --net somenetwork -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:tag
```

- Running in Production Mode

See Install Elasticsearch with Docker


## logstash

- Pipeline Configuration

It is essential to place your pipeline configuration where it can be found by Logstash. By default, the container will look in /usr/share/logstash/pipeline/ for pipeline configuration files.

In this example we use a bind-mounted volume to provide the configuration via the docker run command:

```
docker run --rm -it -v ~/pipeline/:/usr/share/logstash/pipeline/ docker.elastic.co/logstash/logstash:7.0.0
```

Every file in the host directory ~/pipeline/ will then be parsed by Logstash as pipeline configuration.

If you don’t provide configuration to Logstash, it will run with a minimal config that listens for messages from the Beats input plugin and echoes any that are received to stdout. In this case, the startup logs will be similar to the following:

```
Sending Logstash logs to /usr/share/logstash/logs which is now configured via log4j2.properties.
[2016-10-26T05:11:34,992][INFO ][logstash.inputs.beats    ] Beats inputs: Starting input listener {:address=>"0.0.0.0:5044"}
[2016-10-26T05:11:35,068][INFO ][logstash.pipeline        ] Starting pipeline {"id"=>"main", "pipeline.workers"=>4, "pipeline.batch.size"=>125, "pipeline.batch.delay"=>5, "pipeline.max_inflight"=>500}
[2016-10-26T05:11:35,078][INFO ][org.logstash.beats.Server] Starting server on port: 5044
[2016-10-26T05:11:35,078][INFO ][logstash.pipeline        ] Pipeline main started
[2016-10-26T05:11:35,105][INFO ][logstash.agent           ] Successfully started Logstash API endpoint {:port=>9600}
```

This is the default configuration for the image, defined in /usr/share/logstash/pipeline/logstash.conf. If this is the behaviour that you are observing, ensure that your pipeline configuration is being picked up correctly, and that you are replacing either logstash.conf or the entire pipeline directory.

- Settings

The image provides several methods for configuring settings. The conventional approach is to provide a custom logstash.yml file, but it’s also possible to use environment variables to define settings.

- Bind-mounted settings files

Settings files can also be provided through bind-mounts. Logstash expects to find them at /usr/share/logstash/config/.

It’s possible to provide an entire directory containing all needed files:

```
docker run --rm -it -v ~/settings/:/usr/share/logstash/config/ docker.elastic.co/logstash/logstash:7.0.0
```

Alternatively, a single file can be mounted:

```
docker run --rm -it -v ~/settings/logstash.yml:/usr/share/logstash/config/logstash.yml docker.elastic.co/logstash/logstash:7.0.0
```

- Custom Images

Bind-mounted configuration is not the only option, naturally. If you prefer the Immutable Infrastructure approach, you can prepare a custom image containing your configuration by using a Dockerfile like this one:

```
FROM docker.elastic.co/logstash/logstash:7.0.0
RUN rm -f /usr/share/logstash/pipeline/logstash.conf
ADD pipeline/ /usr/share/logstash/pipeline/
ADD config/ /usr/share/logstash/config/
```

Be sure to replace or delete logstash.conf in your custom image, so that you don’t retain the example config from the base image.

- Environment variable configuration

Under Docker, Logstash settings can be configured via environment variables. When the container starts, a helper process checks the environment for variables that can be mapped to Logstash settings. Settings that are found in the environment are merged into logstash.yml as the container starts up.

For compatibility with container orchestration systems, these environment variables are written in all capitals, with underscores as word separators

Some example translations are shown here:

Table 1. Example Docker Environment Variables

```
Environment Variable        Logstash Setting
PIPELINE_WORKERS            pipeline.workers
LOG_LEVEL                   log.level
XPACK_MONITORING_ENABLED    xpack.monitoring.enabled
```

In general, any setting listed in the settings documentation can be configured with this technique.

Note:Defining settings with environment variables causes logstash.yml to be modified in place. This behaviour is likely undesirable if logstash.yml was bind-mounted from the host system. Thus, it is not recommended to combine the bind-mount technique with the environment variable technique. It is best to choose a single method for defining Logstash settings.

- Docker defaults

The following settings have different default values when using the Docker images:

```
http.host                               0.0.0.0
xpack.monitoring.elasticsearch.hosts    http://elasticsearch:9200
```

Note:The setting xpack.monitoring.elasticsearch.hosts is not defined in the -oss image.

These settings are defined in the default logstash.yml. They can be overridden with a custom logstash.yml or via environment variables.

- IMPORTANT

If replacing logstash.yml with a custom version, be sure to copy the above defaults to the custom file if you want to retain them. If not, they will be "masked" by the new file.

- Logging Configuration

Under Docker, Logstash logs go to standard output by default. To change this behaviour, use any of the techniques above to replace the file at /usr/share/logstash/config/log4j2.properties.

## kibana

- Copy and paste to pull this image

```
docker pull kibana:7.0.0
```

- Running in Development Mode

In the given example, Kibana will a attach to a user defined network (useful for connecting to other services (e.g. Elasticsearch)). If network has not yet been created, this can be done with the following command:

```
docker network create somenetwork
```

Note:In this example, Kibana is using the default configuration and expects to connect to a running Elasticsearch instance at http://localhost:9200

Run Kibana

```
docker run -d --name kibana --net somenetwork -p 5601:5601 kibana:tag
```

Kibana can be accessed by browser via http://localhost:5601 or http://host-ip:5601

- Running in Production Mode

For additional information on running and configuring Kibana on Docker, see Running Kibana on Docker
