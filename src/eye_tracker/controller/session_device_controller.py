#-*- coding:utf-8 -*-
"""
session_device_controller

FUNCTION:
    把多个文件聚合到一个文件中
    (1) get_gaze_data
    (2) get_fixation_data
    (3) get_event_data
    (4) get_dynamicobj_data
    (5) get_sensor_data

"""
import time
import os,sys
import json
import random
#config
import config.web_server_config as wsg
import config.session_device_config as cg
#server
from flask import Flask,Blueprint,request,render_template,session
#model
from model.session_device_model import *
from model.dynamic_obj_device_model import *
from model.scene_model import *
from model.participant_model import *

session_device=Blueprint('session_device',__name__)

@session_device.route(cg.get_gaze_data_url,methods=["POST"])
def get_gaze_data(sdk_id_str):
    """
    [POST]
    get_gaze_data
    """
    if request.method=='POST':
        #try:
            try:
                scene_version_number=request.args.get("version")
            except:
                return "error"
            parm=json.loads(request.get_data())
            #print(parm)
            #查找scene_version_id，sv_resource_folder_path
            scene_version_id,_=scene_version_search_by_sdk_id_str_model(sdk_id_str,scene_version_number)
            if scene_version_id is None:
                return "error"
            part=parm["part"]
            if part==1:
                session_id=parm["sessionid"]
                try:
                    session_name=parm["properties"]["c3d.sessionname"]
                except:
                    session_name=random_session_name()
                try:
                    hmdtype=parm["hmdtype"]
                except:
                    hmdtype="unknown"
                interval=parm["interval"]
                formatversion=parm["formatversion"]
                userid=parm["userid"]
                properties_json=json.dumps(parm["properties"])
                session_start_time=int(parm["timestamp"])
                #查询session是否存在如果存在更新不存在创建
                sid=session_insert_update_gaze_model(session_id,session_name,hmdtype,interval,formatversion,userid,properties_json,session_start_time,scene_version_id)
                #participant
                #查询是否有参与者信息
                participant_id=None
                participant_name=None
                if "c3d.participant.id" in parm["properties"].keys():
                    participant_id=parm["properties"]["c3d.participant.id"]
                    try:
                        participant_name=parm["properties"]["c3d.participant.name"]
                    except:
                        participant_name="omit"
                    #获取org_id
                    org_id=organization_id_from_scene_version_id(scene_version_id)
                    if org_id==-1:
                        pass
                    else:
                        create_or_update_participant(participant_id,participant_name,org_id,sid)
                else:
                    pass
            else:
                session_id=parm["sessionid"]
                sid=session_search_by_session_id(session_id)
                if sid==-1:
                    time.sleep(0.5)
                    sid=session_search_by_session_id(session_id)
                    if sid==-1:
                        return "error"
            #保存gaze数据到mongodb
            #key不能有"."所以去掉properies
            data_type="gaze"
            parm["properties"]=None
            data_id=session_data_json_save_model(parm,data_type)
            #更新数据库中的data_ids_json
            session_update_data_ids_json_model(sid,data_type,data_id)
            return "ok"
            
        #except:
            #return "error"
    else:
        return "error"

@session_device.route(cg.get_fixation_data_url,methods=["POST"])
def get_fixation_data(sdk_id_str):
    """
    [POST]
    get_fixation_data
    """
    if request.method=='POST':
        #try:
        parm=json.loads(request.get_data())
        session_id=parm["sessionid"]
        scene_version_number=request.args.get("version")
        scene_version_id,_=scene_version_search_by_sdk_id_str_model(sdk_id_str,scene_version_number)
        data_type="fixation"
        data_id=session_data_json_save_model(parm,data_type)
        session_update_data_ids_json_else_insert_model(session_id,data_id,data_type)
        return "ok"
        #except:
            #return "error"
        #parm=json.loads(request.get_data())
    else:
        return "error"

@session_device.route(cg.get_event_data_url,methods=["POST"])
def get_event_data(sdk_id_str):
    """
    [POST]
    get_event_data
    """
    if request.method=='POST':
        #try:
            parm=json.loads(request.get_data())
            session_id=parm["sessionid"]
            scene_version_number=request.args.get("version")
            scene_version_id,_=scene_version_search_by_sdk_id_str_model(sdk_id_str,scene_version_number)
            data_type="event"
            data_id=session_data_json_save_model(parm,data_type)
            session_update_data_ids_json_else_insert_model(session_id,data_id,data_type)
            set_mysql_session_event(session_id,parm)
            return "ok"
        #except:
            #return "error"
    else:
        return "error"

@session_device.route(cg.get_dynamicobj_data_url,methods=["POST"])
def get_dynamicobj_data(sdk_id_str):
    """
    [POST]
    get_dynamicobj_data
    """
    if request.method=='POST':
        parm=json.loads(request.get_data())
        session_id=parm["sessionid"]
        scene_version_number=request.args.get("version")
        scene_version_id,_=scene_version_search_by_sdk_id_str_model(sdk_id_str,scene_version_number)
        data_type="dynamicobj"
        data_id=session_data_json_save_model(parm,data_type)
        session_update_data_ids_json_else_insert_model(session_id,data_id,data_type)
        return "ok"
    else:
        return "error"

