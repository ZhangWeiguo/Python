# -*-encoding:utf8-*-

import web,os
web.config.debug = False

urls = (
    '/set', 'set',
    '/get', 'get'
)

app = web.application(urls, globals())

web.config.session_parameters['cookie_name'] = 'session_id'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 86400
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = True
web.config.session_parameters['secret_key'] = 'MaolongxiaIsDog'
web.config.session_parameters['expired_message'] = 'Session expired'

if web.config.get('_session') is None:
    session = web.session.Session(app,web.session.DiskStore('sessions'),initializer={"name":"zhangweiguo"})
else:
    session = web.config._session

class set:
    def GET(self):
        web.setcookie("name", "zhangsan", expires=20, domain=None, secure=False)
        print session.name
        return  u"hello MLX!"

class get:
    def GET(self):
        print web.cookies().get("name")
        return  u"hello MLX!"

def test_app():
    app.run()


def test_db():
    from db.db import DB
    db = DB(user_name = 'zhangweiguo', password = 'Python520', database = 'blogs')
    # a = db.AddUser(name = 'zhangsan',password = '1234',age = 99,image = '',description = 'I am a good girl')
    # a = db.AddPaper(user=2,title="Eat As a Fat girl",content='What! Fuck! The meat saled out!')
    # a = db.SelectPaper(1)
    a = db.DeletePaper(3)
    # for i in a:
    #     print i.keys()
    #     print i['id'],i['user'],i['content']

if __name__ == "__main__":
    test_app()


