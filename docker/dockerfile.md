# Dockerfile
```
# This my first nginx Dockerfile
# Version 1.0

# Base images (scratch, busybox, alpine, centos, ubuntu, debian)
FROM centos

#MAINTAINER (author)
MAINTAINER sun 

#ENV (set env)
ENV PATH $PATH:/usr/local/nginx/sbin

#ADD (copy and extract)
ADD nginx.tar.gz /usr/local/  
ADD epel-release-latest-7.noarch.rpm /usr/local/  

#RUN (run os command)
RUN rpm -iv /usr/local/epel-release-latest-7.noarch.rpm
RUN yum install -y wget lftp gcc gcc-c++ make openssl-devel pcre-devel pcre && yum clean all
RUN useradd -s /sbin/nologin -M www

#WORKDIR (like cd)
WORKDIR /usr/local/nginx

RUN ./configure --prefix=/usr/local/nginx --user=www --group=www --with-http_ssl_module --with-pcre && make && make install

RUN echo "daemon off;" >> /etc/nginx.conf

#EXPOSE 映射端口
EXPOSE 80

#CMD 运行以下命令
CMD ["nginx"]
```

# base image
|镜像名称|大小|使用场景|
|---|---|---|
|scratch|0MB|空镜像，系统保留|
|busybox|1.15MB|临时测试用|
|alpine|4.41MB|主要用于测试，也可用于生产环境|
|centos|200MB|主要用于生产环境，支持CentOS/Red Hat，常用于追求稳定性的企业应用|
|ubuntu|81.1MB|主要用于生产环境，常用于人工智能计算和企业应用|
|debian|101MB|主要用于生产环境|

# command
|指令|说明|
|---|---|
|FROM|指定所创建镜像的基础镜像|
|MAINTAINER|指定维护者信息|
|RUN|运行命令|
|CMD|指定启动容器时默认执行的命令|
|LABEL|指定生成镜像的元数据标签信息|
|EXPOSE|声明镜像内服务所监听的端口|
|ENV|指定环境变量|
|ADD|赋值指定的路径下的内容到容器中的路径下，可以为URL；如果为tar文件，会自动解压到路径下|
|COPY|赋值本地主机的路径下的内容到容器中的路径下；一般情况下推荐使用COPY而不是ADD|
|ENTRYPOINT|指定镜像的默认入口|
|VOLUME|创建数据挂载点|
|USER|指定运行容器时的用户名或UID|
|WORKDIR|配置工作目录|
|ARG|指定镜像内使用的参数(例如版本号信息等)|
|ONBUILD|配置当前所创建的镜像作为其他镜像的基础镜像时，所执行的创建操作的命令|
|STOPSIGNAL|容器退出的信号|
|HEALTHCHECK|如何进行健康检查|
|SHELL|指定使用SHELL时的默认SHELL类型|

## FROM : 指定基础镜像，要在哪个镜像建立

> 格式为 FROM <image> 或FROM <image>:<tag>

第一条指令必须为 FROM 指令。FROM命令会指定镜像基于哪个基础镜像创建，接下来的命令也会基于这个基础镜像（CentOS和Ubuntu有些命令可是不一样的）。FROM命令可以多次使用，表示会创建多个镜像。

## MAINTAINER：指定维护者信息

> 格式为 MAINTAINER <name>

## ARG

指定一些镜像内使用的参数(例如版本号信息等)，这些参数在执行docker build命令时才以--build-arg<varname>=<value>格式传入。

> 格式为：ARG<name>[=<default value>]

则可以用docker build --build-arg<name>=<value>来指定参数值。

## RUN：在镜像中要执行的命令

> 格式为 RUN <command> 或 RUN ["executable", "param1", "param2"]

前者默认将在 shell 终端中运行命令，即 /bin/bash -c ；后者则使用 exec 执行。指定使用其它终端可以通过第二种方式实现，例如 RUN [“/bin/bash”, “-c”,”echo hello”] 。

每条RUN指令将在当前镜像的基础上执行指定命令，并提交为新的镜像。当命令较长时可以使用\换行。例如：

```
RUN apt update \
        && apt-get install -y libsnappy-dev zliblg-dev \
        && rm -rf /var/cache/apt
```

## WORKDIR：指定当前工作目录，相当于 cd

> 格式为 WORKDIR /path/to/workdir

为后续的 RUN 、 CMD 、 ENTRYPOINT 指令配置工作目录。
可以使用多个 WORKDIR 指令，后续命令如果参数是相对路径，则会基于之前命令指定的路径。例如

```
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd
```
则最终路径为 /a/b/c 。

## EXPOSE：指定容器要打开的端口

> 格式为 EXPOSE <port> [<port>...]

告诉 Docker 服务端容器暴露的端口号，供互联系统使用。在启动容器时需要通过 -P，Docker 主机会自动分配一个端口转发到指定的端口。

注意：
该命令只是起到声明租用，并不会自动完成端口映射。
在容器启动时需要使用-P(大写P)，Docker主机会自动分配一个宿主机未被使用的临时端口转发到指定的端口；使用-p(小写p)，则可以具体指定哪个宿主机的本地端口映射过来。

## ENV：定义环境变量

> 格式为 ENV <key> <value> 。 指定一个环境变量，会被后续 RUN 指令使用，并在容器运行时保持。

指令指定的环境变量在运行时可以被覆盖掉，如docker run --env <key>=<value> built_image。

## COPY ：复制本地主机的 （为 Dockerfile 所在目录的相对路径）到容器中的

> 格式为 COPY <src> <dest>

## ADD：相当于 COPY，但是比 COPY 功能更强大

> 格式为 ADD <src> <dest>

该命令将复制指定的 到容器中的 。 其中<src> 可以是Dockerfile所在目录的一个相对路径；也可以是一个 URL；还可以是一个 tar 文件，复制进容器会自动解压。
<dest>可以使镜像内的绝对路径，或者相当于工作目录(WORKDIR)的相对路径。路径支持正则表达式，例如：

```
ADD *.c /code/
```

## VOLUME：挂载目录

> 格式为VOLUME ["/data"]

创建一个可以从本地主机或其他容器挂载的挂载点，一般用来存放数据库和需要保持的数据等。

## USER

> 格式为 USER daemon

指定运行容器时的用户名或 UID，后续的 RUN 也会使用指定用户。当服务不需要管理员权限时，可以通过该命令指定运行用户。并且可以在之前创建所需要的用户，例如： RUN useradd -s /sbin/nologin -M www。

## LABEL

LABEL指令用来生成用于生成镜像的元数据的标签信息。

> 格式为：LABEL <key>=<value> <key>=<value> <key>=<value> ...

```
LABEL version="1.0"
LABEL description="This text illustrates \ that label-values can span multiple lines."
```

## ENTRYPOINT

指定镜像的默认入口命令，该入口命令会在启动容器时作为根命令执行，所有传入值作为该命令的参数。

两种格式：

```
ENTRYPOINT ["executable", "param1", "param2"]
 
ENTRYPOINT command param1 param2 （shell 中执行）
```

此时，CMD指令指定值将作为根命令的参数。每个Dockerfile中只能有一个ENTRYPOINT，当指定多个时，只有最后一个有效。在运行时可以被--entrypoint参数覆盖掉，如docker run --entrypoint。

## CMD

支持三种格式

```
CMD ["executable","param1","param2"] 使用 exec 执行，推荐方式；
CMD command param1 param2 在 /bin/bash 中执行，提供给需要交互的应用；
CMD ["param1","param2"] 提供给 ENTRYPOINT 的默认参数；
```

指定启动容器时执行的命令，每个 Dockerfile 只能有一条 CMD 命令。如果指定了多条命令，只有最后一条会被执行。如果用户启动容器时候指定了运行的命令，则会覆盖掉 CMD 指定的命令。

## ONBUILD：在构建本镜像时不生效，在基于此镜像构建镜像时生效

> 格式为 ONBUILD [INSTRUCTION]

配置当所创建的镜像作为其它新创建镜像的基础镜像时，所执行的操作指令。

## STOPSIGNAL

指定所创建镜像启动的容器接收退出的信号值。例如

```
STOPSIGNAL singnal
```

## HEALTHCHECK

配置所启动容器如何进行健康检查(如何判断是否健康)，自Docker 1.12开始支持。

格式有两种：

```
1.HEALTHCHECK [OPTIONS] CMD command    ：根据所执行命令返回值是否为0判断；
2.HEALTHCHECK NONE    　　　　　　　　　　:禁止基础镜像中的健康检查。
```

\[OPTION\]支持：

```
--interval=DURATION  (默认为：30s)：多久检查一次；
--timeout=DURATION  (默认为：30s)：每次检查等待结果的超时时间；
--retries=N 　　     (默认为：3)：如果失败了，重试几次才最终确定失败。
```

CMD关键字后面可以跟执行shell脚本的命令或者exec数组。CMD后面的命令执行完的返回值代表容器的运行状况，可能的值：0 health状态，1 unhealth状态，2 reserved状态

比如，我们启动一个http服务，我们可以这样写健康检查。

## SHELL

指定其他命令使用shell时的默认shell类型。

> 格式为： SHELL ["executable","parameters"]

默认值为 ["bin/sh","-c"]

注意：
对于Windows系统，建议在Dockerfile开头添加# escape=`来指定转移信息。

ENTRYPOINT 和 CMD 的区别：ENTRYPOINT 指定了该镜像启动时的入口，CMD 则指定了容器启动时的命令，当两者共用时，完整的启动命令像是 ENTRYPOINT + CMD 这样。使用 ENTRYPOINT 的好处是在我们启动镜像就像是启动了一个可执行程序，在 CMD 上仅需要指定参数；另外在我们需要自定义 CMD 时不容易出错。

使用 CMD 的 Dockerfile：

```
[root@sta2 test]# cat Dockerfile 
FROM mysql

CMD ["echo","test"]
```

使用 ENTRYPOINT 的 Dockerfile：

```
[root@sta2 entrypoint]#  cat  Dockerfile 
FROM mysql
 
ENTRYPOINT ["echo","test"]
```

结论：ENTRYPOINT 不能覆盖掉执行时的参数，CMD 可以掉覆盖默认的参数。

可以使用以下命令覆盖默认的参数，方便调试 Dockerfile 中的 bug：

```
docker run -it --entrypoint=/bin/bash centos:7
```