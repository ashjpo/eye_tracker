#-*- coding:utf-8 -*-
"""
objective_controller

FUNCTION:
    (1) objective_list*
        objectives列表
        【同】https://api.cognitive3d.com/v0/projects/232/objectives

    (2) objective_create*
        创建objectives（初次创建）
        【同】https://api.cognitive3d.com/v0/versions/1888/objectives

    (3) objective_create_version*
        创建objectives（创建新版本）
        【同】https://api.cognitive3d.com/v0/versions/1888/objectives/58/versions

    (3) objective_delete
        删除某个objectives的版本
        【同】https://api.cognitive3d.com/v0/versions/1888/objectives/58

    (4) objective_detail*
        objectives详情
        【同】https://api.cognitive3d.com/v0/versions/1887/objectives/57

    (5) objective_version_result[TODO]
        objectives某个版本的分析结果(总体)
        【同】https://api.cognitive3d.com/v0/versions/1887/objectiveVersions/112/results

    (6) objective_version_stepresult[TODO]
        objectives某个版本的分析结果(分步)
        【同】https://api.cognitive3d.com/v0/versions/1887/objectiveVersions/112/stepResults

"""
import time
import os,sys
import json
import random
#config
import config.web_server_config as wsg
import config.objective_config as cg
#server
from flask import Flask,Blueprint,request,render_template,session
#model
from model.objective_model import *
from model.scene_model import *

objective=Blueprint('objective',__name__)

@objective.route(cg.objective_create_url,methods=["POST"])
def objective_create():
    """
    [POST]
    objective_create
    """
    if request.method=='POST':
        try:
            parm=json.loads(request.get_data())
        except:
            return "error1"
        #搜索scene_version_id
        scene_version_id=scene_version_id_search_by_sceneidstr_vnumber(parm["scene_id_str"],parm["scene_version_number"])
        if scene_version_id==-1:
            return "error2"
        #创建objective
        objective_id=objective_create_model(scene_version_id,parm["name"],parm["description"])
        if objective_id==-1:
            return "error3"
        #创建objective_version
        is_active=True
        step_json=parm["steps"]
        objective_version_id=objective_version_create_model(objective_id,is_active,step_json)
        if objective_version_id==-1:
            return "error4"
        
        #获取objective的基本信息
        objective_basic_mes=objective_basic_mes_model(objective_id)

        return json.dumps(objective_basic_mes)
    else:
        return "error"

@objective.route(cg.objective_create_version_url,methods=["POST"])
def objective_create_version(scene_version_id,objective_id):
    """
    [POST]
    objective_create_version
    """
    if request.method=='POST':
        try:
            parm=json.loads(request.get_data())
        except:
            return "error"

        #创建objective_version
        is_active=True
        step_json=parm["steps"]
        objective_version_id=objective_version_create_model(objective_id,is_active,step_json)
        if objective_version_id==-1:
            return "error"
        
        #获取objective的基本信息
        objective_basic_mes=objective_basic_mes_model(objective_id)

        return json.dumps(objective_basic_mes)
    else:
        return "error"

@objective.route(cg.objective_detail_url,methods=["GET"])
def objective_detail(scene_version_id,objective_id):
    """
    [GET]
    objective_detail
    """
    if request.method=='GET':
        #获取objective的基本信息
        objective_basic_mes=objective_basic_mes_model(objective_id)
        return json.dumps(objective_basic_mes)
    else:
        return "error"

@objective.route(cg.objective_list_url,methods=["GET"])
def objective_list(project_id):
    """
    [GET]
    objective_list
    """
    if request.method=='GET':
        #获取project下的objective_id
        objective_id_list=get_objective_id_model(project_id)
        objective_mes_list=[]
        for objective_id in objective_id_list:
            objective_basic_mes=objective_basic_mes_model(objective_id)
            objective_mes_list.append(objective_basic_mes)
        return json.dumps(objective_mes_list)
    else:
        return "error"


@objective.route(cg.objective_delete_url,methods=["GET"])
def objective_delete():
    """
    [GET]
    删除某个objective(不具体实现)
    """
    return "[Please contact the administrator!]"

@objective.route(cg.objective_version_stepresult_url,methods=["GET"])
def objective_version_stepresult(scene_version_id,objective_version_id):
    """
    [GET]
    objective_version_stepresult
    """
    if request.method=='GET':
        #获取objective的基本信息
        objective_mes=objective_version_stepresult_model(scene_version_id,objective_version_id)
        return json.dumps(objective_mes)
    else:
        return "error"

@objective.route(cg.objective_session_result_url,methods=["GET"])
def objective_session_result(session_id):
    """
    [GET]
    objective_session_result
    获取单个session的objective结果
    """
    if request.method=='GET':
        res=objective_session_result_model(session_id)
        return json.dumps(res)
    else:
        return "error"