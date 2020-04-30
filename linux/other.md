# Linux allow remote login

## 1.check service ssh
```
service sshd status
# or
systemctl status sshd
```

## 2.install ssh service
```
apt install ssh
# or
yum install ssh-server ssh-clients
```

## 3.start ssh service
```
/etc/init.d/ssh start
# or
systemctl start sshd
```

## 4.edit ssh config
```
sudo vi /etc/ssh/sshd_config
# PermitRootLogin without-password
PermitRootLogin yes
```

## 5.restart ssh service
```
service ssh restart
# or
systemctl restart sshd
```