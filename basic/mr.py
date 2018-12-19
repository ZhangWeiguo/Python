
'''
virtualenv的使用


HADOOP
    安装
        pip install virtualenv

    新建虚拟环境
        virtualenv pythonwego

    使得虚拟环境的路径为相对路径
        virtualenv --relocatable pythonwego

    激活虚拟环境
        source pythonwego/bin/activate

    如果想退出，可以使用下面的命令
        deactivate

    激活后直接安装各种需要的包
        pip install XXX

    压缩环境包
        tar -czf pythonwego.tar.gz pythonwego

    hadoop提交命令则应该这样
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

    python文件中使用则可以
    import sys
    sys.path.append("myvp/myvp/lib/python2.7")

SPARK
    pip install virtualenv
    cd ~/wego/python
    virtualenv py27
    source py27/bin/avtivate
    pip install numpy
    virtualenv --relocatable py27
    zip -r py27.zip py27

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
        test.py
    
    

'''