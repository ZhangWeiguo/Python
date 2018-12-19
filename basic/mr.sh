# Python虚拟环境使用

    # virtualenv的使用
        #安装
            pip install virtualenv
        #新建虚拟环境
            virtualenv pythonwego
        #使得虚拟环境的路径为相对路径
            virtualenv --relocatable pythonwego
        #激活虚拟环境
            source pythonwego/bin/activate
        #激活后直接安装各种需要的包
            pip install XXX
        #如果想退出，可以使用下面的命令
            deactivate
        # 压缩环境包
            zip -r pythonwego.zip envs/pythonwego
            tar -czf pythonwego.tar.gz pythonwego

    # conda的使用
    # virtual必须保证打包环境和运行环境是一致的，conda可以打包整个运行环境，这样来看conda更强大
    # https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/
        # 下载
            wget "https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda2-5.3.1-Linux-x86_64.sh"
        # 安装
            bash Anaconda2-5.3.1-Linux-x86_64.sh
        # 创建环境
            cd ~/anaconda2
            conda create --name pythonwego  python=2.7 scikit-learn
        # 切换环境
            source bin/activate pythonwego
            pip install numpy
        # 退出环境
            source bin/deactivate pythonwego
        # 压缩
            zip -r pythonwego.zip envs/pythonwego
            tar -czf pythonwego.tar.gz pythonwego

# MapReduce中使用Python
    # Hadoop提交命令则应该这样
    $HADOOP_HOME/bin/hadoop  streaming 
        -D mapred.job.priority='VERY_HIGH' 
        -D mared.job.map.capacity=500
        -D mapred.reduce.tasks=0  
        -D mapred.map.tasks=500
        -input      myInputDirs(你的HDFS路径) 
        -output     myOutputDir(你的HDFS路径) 
        -mapper     "python  yourpythonfile.py"
        -reducer    "python  yourpythonfile.py"
        -file       yourpythonfile.py
        -cacheArchive "/xx/xx/xx/pythonwego.tar.gz#python2.7"
        # -cacheArchive "hdfs:///xx/xx/xx/pythonwego.tar.gz#python2.7"

    # python文件中使用则可以
    import sys
    sys.path.append("myvp/myvp/lib/python2.7")

# Spark中使用Python

    spark-submit \
        --name test \
        --master yarn \
        --deploy-mode cluster \
        --num-executors 10 \
        --executor-memory 1g \
        --executor-cores 7 \
        --driver-cores 4 \
        --driver-memory 16g \
        --archives xxx/py27.zip \
        --conf spark.driver.maxResultSize=2g \
        --archives /home/webserver/wego/python/py27.zip#py27 \
        --conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=py27/py27/bin/python \
        --conf spark.yarn.appMasterEnv.PYSPARK_DRIVER_PYTHON=py27/py27/bin/python \
        test.py



