#-*- coding:utf-8 -*-
"""
scene_controller

FUNCTION:
    

"""
import time
import os,sys
import json
import random
#config
import config.web_server_config as wsg
import config.scene_config as cg
#server
from flask import Flask,Blueprint,request,render_template,session
#model
from model.scene_model import *
from model.dynamic_obj_device_model import *

scene=Blueprint('scene',__name__)

@scene.route(cg.scene_detail_url,methods=["GET"])
def scene_detail(sdk_id_str):
    """
    [GET]
    scene_detail
    """
    if request.method=='GET':
        scene_detail=scene_detail_model(sdk_id_str)
        return json.dumps(scene_detail)
    else:
        return "error"
@scene.route(cg.scene_delete_url,methods=["GET"])
def scene_delete():
    """
    [GET]
    删除某个scene(不具体实现)
    """
    return "[Please contact the administrator!]"

@scene.route(cg.scene_edit_url,methods=["GET"])
def scene_edit():
    """
    [GET]
    scene更改(不具体实现)
    """
    return "[Please contact the administrator!]"