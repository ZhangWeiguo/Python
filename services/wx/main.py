# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web
from controller.handle import Handle
from controller.home import Home
urls = (
    '/',   'Home',
    '/wx', 'Handle',
)

app = web.application(urls, globals())
application = app.wsgifunc()

if __name__ == '__main__':
    app.run()