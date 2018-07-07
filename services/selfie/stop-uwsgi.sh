#!/bin/bash
appname="selfie-uwsgi.ini"
function killapp()
{
	appname=$1
	pids=`ps -ef | grep $appname | grep -v "grep" | awk '{print $2}'`
	for pid in $pids
	do
		kill -s 9 $pid
		echo "Killed $pid"
	done
}
uwsgi --stop log/uwsgi.pid || killapp $appname
echo "App Is Stopped!"