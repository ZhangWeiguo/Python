appname="selfie-uwsgi"
pids=`ps -ef | grep $appname | grep -v "grep" | awk '{print $2}'`
if [ -n "$pids" ]
then
	echo "App Is Already Running!"
else
	sudo killall -9 uwsgi
	bash start-uwsgi.sh
	echo "App Is Restarted!"
fi
ps -ef | grep $appname