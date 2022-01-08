#-*- coding:utf-8 -*-
"""
project_controller

FUNCTION:
    (1) project_list
        项目列表
        【同】https://api.cognitive3d.com/v0/organizations/108
    
    (2) project_create
        创建项目
        【同】https://api.cognitive3d.com/v0/projects

    (3) project_delete
        删除项目
        【同】https://api.cognitive3d.com/v0/projects/+project_id

    (4) project_edit (不具体实现)
        编辑项目

    (5) project_scene_detail
        场景信息+项目详情
        【同】https://api.cognitive3d.com/v0/projects/254?useImageLocations=true

    (6) project_key
        获取project_key
        PARM:   pro_id,org_account,org_password
        RETURN: project_key

"""
import time
import os,sys
import json
import random
#config
import config.web_server_config as wsg
import config.project_config as cg
#server
from flask import Flask,Blueprint,request,render_template,session
#model
from model.project_model import *

project=Blueprint('project',__name__)

@project.route(cg.project_scene_detail_url,methods=["GET"])
def project_scene_detail():
    """
    [GET]
    场景信息+项目详情
    """
    if request.method=='GET':
        try:
            pro_id=request.args.get("pro_id")
        except:
            return "error"

        project_scene_detail=project_scene_detail_model(pro_id)
        if project_scene_detail is None:
            return "error"
        else:
            return json.dumps(project_scene_detail)
    else:
        return "error"

@project.route(cg.project_list_url,methods=["GET"])
def project_list():
    """
    [GET]
    项目列表
    """
    if request.method=='GET':
        try:
            org_id=request.args.get("org_id")
        except:
            return "error"

        project_list=project_list_model(org_id)
        return json.dumps(project_list)
    else:
        return "error"

@project.route(cg.project_key_url,methods=["GET"])
def project_key():
    """
    [GET]
    project_key
    """
    if request.method=='GET':
        try:
            pro_id=request.args.get("pro_id")
        except:
            return "error"

        project_key=project_key_model(pro_id)
        return project_key
    else:
        return "error"



@project.route(cg.project_create_url,methods=["POST"])
def project_create():
    """
    [GET]
    创建项目
    """
    if request.method=='POST':
        try:
            parm=json.loads(request.get_data())
            org_id=int(parm["organizationId"])
            name=parm["name"]
            try:
                description=parm["description"]
            except:
                description=""
            ptype=parm["type"]
        except:
            return "error"

        #project_key
        project_key=generate_project_key(org_id,name)
        #prefix
        prefix=generate_prefix(org_id,name)
        #创建资源文件夹
        project_resource_folder_path=create_project_resource_folder(name)
        last_insert_id,now_time=project_create_model(org_id,name,description,ptype,project_key,prefix,project_resource_folder_path)
        if last_insert_id is None:
            return "error"
        return_json={}
        return_json["createdAt"]=now_time
        return_json["updatedAt"]=now_time
        return_json["id"]=last_insert_id
        return_json["organizationId"]=org_id
        return_json["name"]=name
        return_json["description"]=description
        return_json["imageLocation"]=None
        return_json["projectType"]=ptype
        return_json["hidden"]=False
        return_json["prefix"]=prefix
        return_json["project_key"]=project_key

        return json.dumps(return_json)

    else:
        return "error"



def create_project_resource_folder(name):
    """
    创建项目的资源文件夹
    """
    project_resource_folder_path=wsg.app_root_path+wsg.resource_file_path+"/"+name
    print("CREATE PROJECT RESOURCE FOLDER",project_resource_folder_path)
    if os.path.exists(project_resource_folder_path)==False:
        os.makedirs(project_resource_folder_path)
    project_resource_scene_folder_path=wsg.app_root_path+wsg.resource_file_path+"/"+name+"/scene"
    if os.path.exists(project_resource_scene_folder_path)==False:
        os.makedirs(project_resource_scene_folder_path)
    project_resource_media_folder_path=wsg.app_root_path+wsg.resource_file_path+"/"+name+"/media_lib"
    if os.path.exists(project_resource_media_folder_path)==False:
        os.makedirs(project_resource_media_folder_path)
    return wsg.resource_file_path+"/"+name

@project.route(cg.project_delete_url,methods=["GET"])
def project_delete():
    """
    [GET]
    删除某个组织下的用户(不具体实现)
    """
    return "[Please contact the administrator!]"

@project.route(cg.project_delete_url,methods=["GET"])
def project_edit():
    """
    [GET]
    用户内容更改(不具体实现)
    """
    return "[Please contact the administrator!]"