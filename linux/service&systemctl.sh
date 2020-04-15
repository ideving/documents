##-----------------------##
## service               ##
## vi /etc/init.d/tomcat ##
##-----------------------##
#!/bin/bash
# description: Tomcat Start Stop Restart
# processname: tomcat
export JAVA_HOME=/opt/jdk
export CLASS_PATH=.:$JAVA_HOME/lib
CATALINA_HOME=/opt/tomcat
case $1 in
        start)
                sh $CATALINA_HOME/bin/startup.sh
                ;;
        stop)
                sh $CATALINA_HOME/bin/shutdown.sh
                ;;
        restart)
                sh $CATALINA_HOME/bin/shutdown.sh
                sh $CATALINA_HOME/bin/startup.sh
                ;;
        *)
                echo 'please use : tomcat {start | stop | restart}'
        ;;
esac
exit 0

##-----------------------##
## service               ##
## vi /etc/init.d/tomcat ##
##-----------------------##
#!/bin/bash
#startup script for tomcat on linux
#filename tomcat.sh
#JAVA_HOME=/opt/jdk
TOMCAT_HOME=/opt/tomcat
start_tomcat=$TOMCAT_HOME/bin/daemon.sh
stop_tomcat=$TOMCAT_HOME/bin/daemon.sh
start() {
    echo -n "Starting tomcat:"
    ${start_tomcat} start
    echo "tomcat start ok"
}
stop() {
    echo -n "Shutdown tomcat"
    ${stop_tomcat} stop
    echo "tomcat stop ok"
}
#how we were called
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 10
        start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
esac
exit 0

##-------------------------------------------##
## systemctl                                 ##
## vi /usr/lib/systemd/system/tomcat.service ##
##-------------------------------------------##

[Unit]
Description=Tomcat
After=syslog.target network.target remote-fs.target nss-lookup.target
[Service]
Type=forking
Environment='JAVA_HOME=/opt/jdk'
Environment='CATALINA_PID=/opt/tomcat/tomcat.pid'
Environment='CATALINA_HOME=/opt/tomcat'
Environment='CATALINA_BASE=/opt/tomcat'
Environment='CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC'
ExecStart=/opt/tomcat/bin/startup.sh
ExecStop=/bin/kill -s QUIT $MAINPID
ExecReload=/bin/kill -s HUP $MAINPID
PrivateTmp=true
RemainAfterExit=yes
WorkingDirectory=/opt/tomcat
[Install]
WantedBy=multi-user.target