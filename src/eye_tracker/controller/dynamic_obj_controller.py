#-*- coding:utf-8 -*-
"""
dynamic_obj_controller

FUNCTION:
    dynamic_obj_list
    group_list[TODO]
    group_analyze_data_list[TODO]
    dynamic_obj_detail

"""
import time
import os,sys
import json
import random
#config
import config.web_server_config as wsg
import config.dynamic_obj_config as cg
#server
from flask import Flask,Blueprint,request,render_template,session
#model
from model.dynamic_obj_model import *

dynamic_obj=Blueprint('dynamic_obj',__name__)

@dynamic_obj.route(cg.dynamic_obj_list_url,methods=["GET"])
def dynamic_obj_list(scene_version_id):
    """
    [GET]
    dynamic_obj_list
    """
    if request.method=='GET':
        dynamic_obj_list=dynamic_obj_list_model(scene_version_id)
        return json.dumps(dynamic_obj_list)
    else:
        return "error"

@dynamic_obj.route(cg.dynamic_obj_detail_url,methods=["GET"])
def dynamic_obj_detail(scene_version_id,dynamic_obj_id):
    """
    [GET]
    dynamic_obj_detail
    """
    if request.method=='GET':
        dynamic_obj_detail=dynamic_obj_detail_model(dynamic_obj_id)
        return json.dumps(dynamic_obj_detail)
    else:
        return "error"