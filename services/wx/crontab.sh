# crontab保活
# * * * * * cd /home/ubuntu/Code/Python/services/wx && bash monitor-uwsgi.sh > /dev/null 2>&1 &
# * * * * * cd /home/ubuntu/Code/Python/services/wx && bash monitor-nginx.sh > /dev/null 2>&1 &
# cmd>file 是标准输出
# /dev/null 是无底洞
# 2>$1 是错误输出也按照前面的规则
# 最后一个&是后台运行