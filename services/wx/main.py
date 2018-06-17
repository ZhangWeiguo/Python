# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web
from controller.handle import Handle

urls = (
    '/',   'Index',
    '/wx', 'Handle',
)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()