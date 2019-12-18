# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_apscheduler import APScheduler

app = Flask(__name__, instance_relative_config=True, template_folder='templates', static_folder='static',
            static_url_path="/web/static")
#import  os
#print os.environ.keys()
#print os.environ.get('FLASKR_SETTINGS')
#加载配置文件内容
#app.config.from_object('web.config')     #模块下的config文件名，不用加py后缀
app.config.from_envvar('FLASKR_SETTINGS')   #环境变量，指向配置文件setting的路径
#app.config.from_pyfile('F:\代吗\py\web-web\web\config.py')

#创建数据库对象
db = SQLAlchemy(app,use_native_unicode="utf8")
# detector = Detector()

mail = Mail(app)
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()


# from web.utils.mail import executeDetection
# executeDetection()

from web.controller import views
# from web.controller import test