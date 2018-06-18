# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web
from controller.wx import Wx
from controller.home import Home
from controller.login import Login
urls = (
    '/',        'Home',
    '/wx',      'Wx',
    '/login',   'Login',
)

app = web.application(urls, globals())
application = app.wsgifunc()

if __name__ == '__main__':
    app.run()