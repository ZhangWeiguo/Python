# -*-encoding:utf-8-*-
'''
created by zwg in 2017-12-24
'''


import web,os,time
from db.db import DB

db = DB(user_name = 'zhangweiguo', password = 'Python520', database = 'blogs')
web.config.debug = False

urls = (
    '/login',        'Login',
    '/register',     'Register',
    '/selfie',       'Selfie',
    '/details',       'Details'
)

app = web.application(urls, globals())
web.config.session_parameters['cookie_name'] = 'session_id'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 1200
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = True
web.config.session_parameters['secret_key'] = 'MaolongxiaIsDog'
web.config.session_parameters['expired_message'] = 'Session expired'

if web.config.get('_session') is None:
    session = web.session.Session(app,web.session.DiskStore('sessions'),initializer={"name":"zhangweiguo"})
else:
    session = web.config._session

class Login:
    def GET(self):
        data = web.input()
        if "userid" in data:
            id = data['userid']
            password = data['password']
            print id,password
            r = db.CheckUser(id,password)
            r = list(r)
            print r
            if len(r) == 0:
                s = os.path.join('template', 'login.html')
                render = web.template.frender(s)
                return render()
            else:
                web.setcookie("name", r[0]['name'], expires=86400, domain=None, secure=False)
                web.setcookie("id", r[0]['id'], expires=86400, domain=None, secure=False)
                web.setcookie("description", r[0]['description'], expires=86400, domain=None, secure=False)
                web.seeother('/selfie')
        else:
            s = os.path.join('template','login.html')
            render = web.template.frender(s)
            return render()

class Register:
    def GET(self):
        data = web.input()
        if "password" in data:
            if str(data["password"]).strip() == "":
                s = os.path.join('template', 'registerfailed.html')
                render = web.template.frender(s)
                return render()
        if "username" in data:
            a = db.AddUser(name=data["username"],
                           password=data["password"],
                           age=data["age"],
                           image='',
                           description=data["sigin"])
            if a != -1:
                web.setcookie("password", data['password'], expires=86400, domain=None, secure=False)
                web.setcookie("id", a, expires=86400, domain=None, secure=False)
                web.seeother("/login")
            else:
                s = os.path.join('template', 'register.html')
                render = web.template.frender(s)
                return render()
        else:
            s = os.path.join('template','register.html')
            render = web.template.frender(s)
            return render()

class Selfie:
    def GET(self):
        name = web.cookies().get("name")
        id = str(web.cookies().get("id"))
        description = web.cookies().get("description")
        s = os.path.join('template', 'selfie.html')
        render = web.template.frender(s)
        print name,id,description
        return render(name,id,description)

class Details:
    def GET(self):
        r = db.SelectAllPaper()
        data = []
        for i in r:
            d = []
            d.append(i['id'])
            d.append(i['user'])
            d.append(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(i['create_time'])))
            d.append(i['title'])
            d.append(i['content'])
            data.append(d)
        s = os.path.join('template', 'papers.html')
        render = web.template.frender(s)
        print data
        return render(data)

app.run()
