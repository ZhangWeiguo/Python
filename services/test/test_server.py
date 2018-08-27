# -*- encoding:utf-8 -*-

'''
安装Package
    pip install web.py
执行程序
    python test_server.py 8080
访问
    http://localhost:8080/file_controller

'''


import web,os

def controll_file(filename1, filename2):
    # 这里写你的处理逻辑，我只是简单把两个文件合并
    filename = "TestFile"
    f =file(filename,'w')
    f1 =file(filename1,'r')
    f2 =file(filename2,'r')
    f.write(f1.read())
    f.write(f2.read())
    f.close()
    f1.close()
    f2.close()
    return filename
    


urls = (
    '/',                    'Index',
    '/file_controller',     'FileController',
)


file_html = '''
<html>
    <head>
        <title>Just A Test</title>
    </head>
    <body>
        <h1>This Is A Test To Control File</h1>
        <form method="POST" enctype="multipart/form-data" action="">
        <input type="file" name="myfile1" />
        <br/>
        <input type="file" name="myfile2" />
        <input type="submit" />
        </form>
    </body>
</html>
'''



class Index:
    def GET(self):
        return "Hello World"

class FileController:
    def GET(self):
        return file_html

    def POST(self):
        data = web.input(myfile1={},myfile2={})

        filepath2 = data.myfile2.filename.replace('\\','/')
        filename2 = filepath2.split('/')[-1]
        filepath1 = data.myfile1.filename.replace('\\','/')
        filename1 = filepath1.split('/')[-1]

        fout = open(filename1,'w')
        fout.write(data.myfile1.file.read())
        fout.close()
        fout = open(filename2,'w')
        fout.write(data.myfile2.file.read())
        fout.close()

        filename = controll_file(filename1, filename2)
        s = 'Your File Is Generated In: ' + filename
        return s
if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
