# -*- coding: utf-8 -*-
# created by zwg in 20180617
import web,os

urls = (
    '/',        'Index',
)

class Index:
    def GET(self):
        s = os.path.join('templates','index.html')
        render = web.template.frender(s)
        return render()
    def POST(self):
        s = os.path.join('templates','index.html')
        render = web.template.frender(s)
        return render()

app = web.application(urls, globals())
application = app.wsgifunc()

if __name__ == '__main__':
    app.run()