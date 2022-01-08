#-*- coding:utf-8 -*-
"""
session_controller

FUNCTION:
    

"""
import time
import os,sys
import json
import random
#config
import config.web_server_config as wsg
import config.session_config as cg
#server
from flask import Flask,Blueprint,request,render_template,session
#model
from model.session_model import *

my_session=Blueprint('my_session',__name__)

@my_session.route(cg.session_list_url,methods=["GET"])
def session_list(scene_version_id):
    """
    [GET]
    session_list
    """
    if request.method=='GET':
        try:
            page=int(request.args.get("page"))
            limit=int(request.args.get("limit"))
        except:
            page=0
            limit=20
        if page is None:
            page=0
        if limit is None:
            limit=20
        session_list=session_list_model(scene_version_id,page,limit)
        return json.dumps(session_list)
    else:
        return "error"

@my_session.route(cg.session_metadata_url,methods=["GET"])
def session_metadata(scene_version_id,sid):
    """
    [GET]
    session_metadata
    """
    if request.method=='GET':
        session_meta=session_metadata_model(sid)
        return json.dumps(session_meta)
    else:
        return "error"

@my_session.route(cg.session_single_queries_url,methods=["POST"])
def session_single_queries():
    """
    [POST]
    session_single_queries
    """
    if request.method=='POST':
        parm=json.loads(request.get_data())
        session_mes=session_single_queries_model(parm)
        return json.dumps(session_mes)
    else:
        return "error"

@my_session.route(cg.session_queries_url,methods=["POST"])
def session_queries():
    """
    [POST]
    session_queries
    """
    if request.method=='POST':
        parm=json.loads(request.get_data())
        session_mes=session_queries_model(parm)
        return json.dumps(session_mes)
    else:
        return "error"

@my_session.route(cg.session_gaze_data_url,methods=["GET"])
def session_gaze_data(scene_version_id,session_id):
    """
    [GET]
    session_gaze_data
    """
    if request.method=='GET':
        session_mes=session_data_model(scene_version_id,session_id,"gaze")
        return json.dumps(session_mes)
    else:
        return "error"

@my_session.route(cg.session_fixation_data_url,methods=["GET"])
def session_fixation_data(scene_version_id,session_id):
    """
    [GET]
    session_fixation_data
    """
    if request.method=='GET':
        session_mes=session_data_model(scene_version_id,session_id,"fixation")
        return json.dumps(session_mes)
    else:
        return "error"

@my_session.route(cg.session_event_data_url,methods=["GET"])
def session_event_data(scene_version_id,session_id):
    """
    [GET]
    session_event_data
    """
    if request.method=='GET':
        session_mes=session_data_model(scene_version_id,session_id,"event")
        return json.dumps(session_mes)
    else:
        return "error"

@my_session.route(cg.session_dynamicobj_data_url,methods=["GET"])
def session_dynamicobj_data(scene_version_id,session_id):
    """
    [GET]
    session_dynamicobj_data
    """
    if request.method=='GET':
        session_mes=session_data_model(scene_version_id,session_id,"dynamicobj")
        return json.dumps(session_mes)
    else:
        return "error"

@my_session.route(cg.session_slicer_field_queries_url,methods=["POST"])
def session_slicer_field_queries():
    """
    [POST]
    session_slicer_field_queries
    EVENT
    """
    if request.method=='POST':
        parm=json.loads(request.get_data())
        pro_id=parm["entityFilters"]["projectId"]
        if parm["field"]["fieldName"]=="eventName":
            session_mes=session_slicer_field_queries_event_model(pro_id)
        return json.dumps(session_mes)
    else:
        return "error"

@my_session.route(cg.session_slicer_metric_object_queries_url,methods=["POST"])
def session_slicer_metric_object_queries():
    """
    [POST]
    session_slicer_metric_object_queries
    """
    if request.method=='POST':
        parm=json.loads(request.get_data())
        session_mes=session_slicer_metric_object_queries_model(parm)
        return json.dumps(session_mes)
    else:
        return "error"

@my_session.route(cg.session_slicer_metric_group_queries_url,methods=["POST"])
def session_slicer_metric_group_queries():
    """
    [POST]
    session_slicer_metric_group_queries
    """
    if request.method=='POST':
        parm=json.loads(request.get_data())
        session_mes=session_slicer_metric_group_queries_model(parm)
        return json.dumps(session_mes)
    else:
        return "error"

@my_session.route(cg.dynamic_obj_cube_agg_queries_url,methods=["POST"])
def dynamic_obj_cube_agg_queries():
    """
    [POST]
    dynamic_obj_cube_agg_queries
    """
    if request.method=='POST':
        parm=json.loads(request.get_data())
        session_mes=dynamic_obj_cube_agg_queries_model(parm)
        return json.dumps(session_mes)
    else:
        return "error"

@my_session.route(cg.session_slicer_queries_url,methods=["POST"])
def session_slicer_queries():
    """
    [POST]
    session_slicer_queries
    """
    if request.method=='POST':
        parm=json.loads(request.get_data())
        session_mes=session_slicer_queries_model(parm)
        return json.dumps(session_mes)
    else:
        return "error"