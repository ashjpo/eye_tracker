#-*- coding:utf-8 -*-
"""
用于实现web后端响应
"""

import time
import os,sys
import json
import random
#config
import config.web_server_config as wsg
#server
from gevent import monkey
from gevent.pywsgi import WSGIServer
import socket
from flask import Flask,Blueprint,request,render_template,session
#controller
from controller.admin_controller import *
from controller.project_controller import *
from controller.scene_device_controller import *
from controller.dynamic_obj_device_controller import *
from controller.session_device_controller import *
from controller.scene_controller import *
from controller.dynamic_obj_controller import *
from controller.objective_controller import *
from controller.session_controller import *
from controller.category_controller import *
from controller.participant_controller import *



monkey.patch_all()
# gevent end
app = Flask(__name__,static_folder="resource")
app.config.update(
    DEBUG=True
)
app.config['SECRET_KEY'] = os.urandom(24)

#注册控制器
app.register_blueprint(admin)
app.register_blueprint(project)
app.register_blueprint(scene_device)
app.register_blueprint(dynamic_obj_device)
app.register_blueprint(session_device)
app.register_blueprint(scene)
app.register_blueprint(dynamic_obj)
app.register_blueprint(objective)
app.register_blueprint(my_session)
app.register_blueprint(category)
app.register_blueprint(participant)


def start():
    """
    用于启动webserver
    """
    temp_host=wsg.web_host
    http_server = WSGIServer((str(temp_host), wsg.web_port), app)
    http_server.serve_forever()

@app.route("/test_page")
def test_page():
    """
    测试页面
    """
    return "ok"




    

if __name__ == '__main__':
    start()
