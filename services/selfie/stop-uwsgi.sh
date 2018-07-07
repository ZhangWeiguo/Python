#!/bin/bash
# function killapp()
# {
# 	appname=$1
# 	pids=`ps -ef | grep $appname | grep -v "grep" | awk '{print $2}'`
# 	for pid in $pids
# 	do
# 		kill -s 9 $pid
# 		echo "Killed $pid"
# 	done
# }
# appname=`cat app.ini | grep "procname-master" | awk '{print $3}'`
# killapp $appname
# echo "App Is Stopped!"
uwsgi --stop log/uwsgi.pid