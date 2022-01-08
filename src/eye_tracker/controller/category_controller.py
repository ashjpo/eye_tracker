#-*- coding:utf-8 -*-
"""
category_controller

FUNCTION:
    

"""
import time
import os,sys
import json
import random
#config
import config.web_server_config as wsg
import config.category_config as cg
#server
from flask import Flask,Blueprint,request,render_template,session
#model
from model.category_model import *

category=Blueprint('category',__name__)


@category.route(cg.set_obj_category_url,methods=["POST"])
def set_obj_category(scene_version_id):
    """
    [POST]
    set_obj_category
    {"name":"test_group4"}
    {"categoryId":2034,"name":"g2"}
    """
    if request.method=='POST':
        try:
            parm=json.loads(request.get_data())
        except:
            return "error"
        if ("categoryId" in parm.keys()) and ("name" in parm.keys()):
            #创建group
            last_insert_id=create_group_model(parm["categoryId"],parm["name"])
            #获取category详情
            category_mes=category_detail_model(parm["categoryId"])
            return json.dumps(category_mes)
        elif "name" in parm.keys():
            #创建category
            last_insert_id=create_category_model(parm["name"],scene_version_id)
            if last_insert_id==-1:
                return "error"
            #获取category详情
            category_mes=category_detail_model(last_insert_id)
            return json.dumps(category_mes)
    else:
        return "error"

@category.route(cg.set_dobj_to_group_url,methods=["POST"])
def set_dobj_to_group(group_id,dobj_id):
    """
    [POST]
    set_dobj_to_group
    """
    if request.method=='POST':
        try:
            parm=json.loads(request.get_data())
        except:
            return "error"
        set_dobj_to_group_model(parm,group_id)
        
        return "ok"
    else:
        return "error"

@category.route(cg.get_obj_category_list_url,methods=["GET"])
def get_obj_category_list(scene_version_id):
    """
    [GET]
    get_obj_category_list
    """
    if request.method=='GET':
        res=get_obj_category_list_model(scene_version_id)
        
        return json.dumps(res)
    else:
        return "error"