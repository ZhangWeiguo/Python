appname="wx-uwsgi.ini"
pids=`ps -ef | grep $appname | grep -v "grep" | awk '{print $2}'`
if [ -n "$pids" ]
then
	echo "App Is Already Running!"
else
	sudo uwsgi $appname
	echo "App Is Restarted!"
fi
ps -ef | grep $appname
# * * * * * cd /home/ubuntu/Code/Python/services/wx && bash monitor.sh > /dev/null 2>&1 &