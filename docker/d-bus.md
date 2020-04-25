#### ERROR: Failed to get D-Bus connection: Operation not permitted

```
#centos
docker run --name centos -dit --privileged=true centos:8 /usr/sbin/init
docker exec -it centos bash
systemctl start xxx.service
```