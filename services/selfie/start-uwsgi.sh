#!/bin/bash
set -e
appname="selfie-uwsgi.ini"
echo "AppName : $appname"
pids=`ps -ef | grep $appname | grep -v "grep" | awk '{print $2}'`
if [ -n "$pids" ]
then
	echo "App Is Already Running"
else
	uwsgi selfie-uwsgi.ini
	echo "App Is Running"
fi
ps -ef | grep $appname
