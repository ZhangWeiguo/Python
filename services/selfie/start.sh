#/bin/bash
set -e
appname=`cat app.ini | grep "procname-master" | awk '{print $3}'`
echo "AppName : $appname"
pids=`ps -ef | grep $appname | grep -v "grep" | awk '{print $2}'`
if [ -n "$pids" ]
then
	echo "App Is Already Running"
else
	uwsgi app.ini
	echo "App Is Running"
fi
ps -ef | grep $appname
