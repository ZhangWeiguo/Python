appname="wx-nginx.conf"
pids=`ps -ef | grep $appname | grep -v "grep" | awk '{print $2}'`
if [ -n "$pids" ]
then
	echo "App Is Already Running!"
else
	bash start-nginx.sh
	echo "App Is Restarted!"
fi
ps -ef | grep $appname