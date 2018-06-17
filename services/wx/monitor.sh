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
# crontab保活
# * * * * * cd /home/ubuntu/Code/Python/services/wx && bash monitor.sh > /dev/null 2>&1 &
# cmd>file 是标准输出
# /dev/null 是无底洞
# 2>$1 是错误输出也按照前面的规则
# 最后一个&是后台运行