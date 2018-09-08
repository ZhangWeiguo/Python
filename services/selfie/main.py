# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web,os
from controllers.index import Index
from controllers.login import Login
from controllers.user import User
from controllers.cate import Cate
from controllers.blog import Blog
from controllers.catalog import Catalog
from controllers.edit_blog import EditBlog
from controllers.api import API
from controllers.unknow import Unknow

web.config.debug = False

urls = (
    '/',                'Index',
    '/login',           'Login',
    '/user/(.*)',       'User',
    '/cate/(.+)',       'Cate',
    '/blog',            'Blog',
    '/catalog(.+)',     'Catalog',
    '/edit_blog',       'EditBlog',
    '/api',             'API',
    '/(.*)',            'Unknow',
)

# ToDo
#       Session
#       Login
#       Paper
#       Comment
#       Others

web.config.session_parameters['cookie_name']        = 'session_id'
web.config.session_parameters['cookie_domain']      = None
web.config.session_parameters['timeout']            = 120000
web.config.session_parameters['ignore_expiry']      = True
web.config.session_parameters['ignore_change_ip']   = True
web.config.session_parameters['secret_key']         = 'MaolongxiaIsDog'
web.config.session_parameters['expired_message']    = 'Session expired'

app = web.application(urls, globals())
session_store = web.session.DiskStore('sessions')
session = web.session.Session(app, session_store, initializer={"user_name":"","pass_word":""})
web.config.session = session

application = app.wsgifunc()

if __name__ == '__main__':
    app.run()