#-*- coding:utf-8 -*-
"""
project_controller

FUNCTION:
    (1) get_scene_setting
        获取场景设置
        【同】/v0/scenes/2836bfbc-9a81-46e6-bf66-6598c49b4ea3

    (2) upload_new_scene
        上传新场景（第一次上传）【***加project_id***】
        【同】/v0/scenes

    (3) upload_new_version_scene
        更新上传场景（非第一次上传）
        【同】/v0/scenes/2836bfbc-9a81-46e6-bf66-6598c49b4ea3/screenshot?version=2

    (4) upload_screen_shot
        上传场景封面
        【同】/v0/scenes/2836bfbc-9a81-46e6-bf66-6598c49b4ea3

"""
import time
import os,sys
import json
import random
#config
import config.web_server_config as wsg
import config.scene_device_config as cg
#server
from flask import Flask,Blueprint,request,render_template,session
#model
from model.scene_device_model import *

scene_device=Blueprint('scene_device',__name__)

@scene_device.route(cg.get_scene_setting_url,methods=["GET"])
def get_scene_setting(sdk_id_str):
    """
    [GET]
    获取场景设置
    """
    if request.method=='GET':
        scene_setting=get_scene_setting_model(sdk_id_str)

        return json.dumps(scene_setting)
    else:
        return "error"

@scene_device.route(cg.upload_screen_shot_url,methods=["POST"])
def upload_screen_shot(sdk_id_str):
    """
    [POST]
    上传场景封面
    """
    #temp_file_dir="../temp"
    if request.method=='POST':
        try:
            scene_version_number=request.args.get("version")
        except:
            return "error"
        file_name_list=[]
        file_list=[]
        #缩略图
        screenshot_image_list=request.files.getlist('screenshot')
        for file in screenshot_image_list:
            file_name_list.append(file.filename)
            file_list.append(file)
        
        #查询scene_id
        scene_version_resource_path=None
        scene_version_resource_path=scene_version_resource_path_search_model(sdk_id_str,scene_version_number)
        if scene_version_resource_path is None:
            return "error"
        #获取上传的文件
        for i in range(len(file_name_list)):
            fname=file_name_list[i]
            file=file_list[i]
            file.save(wsg.app_root_path+scene_version_resource_path+"/scene_view/"+fname)
        return "ok"
    else:
        return "error"

@scene_device.route(cg.upload_new_scene_url,methods=["POST"])
def upload_new_scene():
    """
    [POST]
    上传新场景（第一次上传）
    """
    #temp_file_dir="../temp"
    if request.method=='POST':
        file_name_list=[]
        file_list=[]
        scene_json=None
        #3d文件
        for file in request.files.getlist('file'): # 这里改动以存储多份文件
            if file and allowed_file(file.filename):
                file_name_list.append(file.filename)
                file_list.append(file)
                #通过scene.json文件获取相关信息
                if file.filename=="settings.json":
                    scene_json=json.loads(str(file.read(), encoding = "utf-8"))
        #缩略图
        screenshot_image_list=request.files.getlist('screenshot')
        for file in screenshot_image_list:
            file_name_list.append(file.filename)
            file_list.append(file)

        print(scene_json)
        if scene_json is None:
            return "error"
        scale=scene_json["scale"]
        sdkVersion=scene_json["sdkVersion"]
        scene_name=scene_json["sceneName"]
        project_key=scene_json["ApplicationKey"]
        #if "debug.log"
        if len(file_name_list)<4:
            return "error"
        #查询project相关信息
        project_mes=scene_upload_project_mes_model(project_key)
        if project_mes is None:
            return "error"
        
        #创建scene资源文件夹
        scene_resource_folder_path=create_scene_resource_folder(project_mes["name"],scene_name)
        #创建scene-version资源文件夹
        scenev_resource_folder_path=create_scene_version_resource_folder(project_mes["name"],scene_name)
        
        #获取上传的文件
        for i in range(len(file_name_list)):
            fname=file_name_list[i]
            file=file_list[i]
            file.save(scenev_resource_folder_path+"/scene_view/"+fname)
            if fname=="settings.json":
                with open(scenev_resource_folder_path+"/scene_view/"+fname,'w') as f:
                    json.dump(scene_json,f)

        sdk_id_str=generate_sdk_id_str(project_mes["name"],scene_name)
        
        #scene插入数据库
        scene_des=""
        pro_id=project_mes["id"]
        customer_id=""
        latest_screenshot_location=""
        resource_folder_path=scene_resource_folder_path.replace(wsg.app_root_path,"")
        scene_id=create_scene_model(scene_name,scene_des,sdk_id_str,pro_id,customer_id,latest_screenshot_location,resource_folder_path)
        if scene_id==-1:
            return "error"
        #scene-version插入数据库
        scene_version_resource_folder_path=scenev_resource_folder_path.replace(wsg.app_root_path,"")
        scene_file_type="gltf"
        mesh_name="scene"
        if len(screenshot_image_list)>0:
            sc_latest_screenshot_location=scene_version_resource_folder_path+"/scene_view/"+screenshot_image_list[0].filename
        else:
            sc_latest_screenshot_location=""
        resource_file_name_json=json.dumps(file_name_list)
        scene_version_id=create_scene_version_model(scene_id,scene_file_type,sdkVersion,scale,mesh_name,sc_latest_screenshot_location,resource_file_name_json,scene_version_resource_folder_path)
        if scene_version_id==-1:
            return "error"
        return sdk_id_str

    else:
        return "error"

@scene_device.route(cg.upload_new_version_scene_url,methods=["POST"])
def upload_new_version_scene(sdk_id_str):
    """
    [POST]
    更新上传场景（非第一次上传）
    """
    #temp_file_dir="../temp"
    if request.method=='POST':
        file_name_list=[]
        file_list=[]
        scene_json=None
        #3d文件
        for file in request.files.getlist('file'): # 这里改动以存储多份文件
            if file and allowed_file(file.filename):
                file_name_list.append(file.filename)
                file_list.append(file)
                #通过scene.json文件获取相关信息
                if file.filename=="settings.json":
                    scene_json=json.loads(str(file.read(), encoding = "utf-8"))
        #缩略图
        screenshot_image_list=request.files.getlist('screenshot')
        for file in screenshot_image_list:
            file_name_list.append(file.filename)
            file_list.append(file)

        print(scene_json)
        if scene_json is None:
            return "error"
        scale=scene_json["scale"]
        sdkVersion=scene_json["sdkVersion"]
        scene_name=scene_json["sceneName"]
        project_key=scene_json["ApplicationKey"]
        #if "debug.log"
        if len(file_name_list)<4:
            return "error"
        #查询project相关信息
        project_mes=scene_upload_project_mes_model(project_key)
        if project_mes is None:
            return "error"
        
        #创建scene-version资源文件夹
        scenev_resource_folder_path=create_scene_version_resource_folder(project_mes["name"],scene_name)
        
        #获取上传的文件
        for i in range(len(file_name_list)):
            fname=file_name_list[i]
            file=file_list[i]
            file.save(scenev_resource_folder_path+"/scene_view/"+fname)
            if fname=="settings.json":
                with open(scenev_resource_folder_path+"/scene_view/"+fname,'w') as f:
                    json.dump(scene_json,f)
        
        #查询scene_id
        scene_id=-1
        scene_id=scene_search_by_sdk_id_str_model(sdk_id_str)
        if scene_id==-1:
            return "error"
        #scene-version插入数据库
        scene_version_resource_folder_path=scenev_resource_folder_path.replace(wsg.app_root_path,"")
        scene_file_type="gltf"
        mesh_name="scene"
        if len(screenshot_image_list)>0:
            sc_latest_screenshot_location=scene_version_resource_folder_path+"/"+screenshot_image_list[0].filename
        else:
            sc_latest_screenshot_location=""
        resource_file_name_json=json.dumps(file_name_list)
        scene_version_id=create_scene_version_model(scene_id,scene_file_type,sdkVersion,scale,mesh_name,sc_latest_screenshot_location,resource_file_name_json,scene_version_resource_folder_path)
        if scene_version_id==-1:
            return "error"
        return sdk_id_str

    else:
        return "error"

ALLOWED_EXTENSIONS=['log','png','jpg','gif','gltf','bin','json']
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def create_scene_resource_folder(project_name,scene_name):
    """
    创建scene的资源文件夹
    """
    scene_resource_folder_path=wsg.app_root_path+wsg.resource_file_path+"/"+project_name+"/scene/"+scene_name
    print("CREATE SCENE RESOURCE FOLDER",scene_resource_folder_path)
    if os.path.exists(scene_resource_folder_path)==False:
        os.makedirs(scene_resource_folder_path)
    return scene_resource_folder_path

def create_scene_version_resource_folder(project_name,scene_name):
    """
    创建scene-version的资源文件夹
    """
    scene_folder=wsg.app_root_path+wsg.resource_file_path+"/"+project_name+"/scene/"+scene_name+"/"
    version_id=1
    for listx in os.listdir(scene_folder):
        if os.path.isdir(scene_folder+listx):
            version_id+=1
    scenev_resource_folder_path=wsg.app_root_path+wsg.resource_file_path+"/"+project_name+"/scene/"+scene_name+"/"+str(version_id)
    print("CREATE SCENE-VERSION RESOURCE FOLDER",scenev_resource_folder_path)
    if os.path.exists(scenev_resource_folder_path)==False:
        os.makedirs(scenev_resource_folder_path)
    if os.path.exists(scenev_resource_folder_path+"/scene_view")==False:
        os.makedirs(scenev_resource_folder_path+"/scene_view")
    if os.path.exists(scenev_resource_folder_path+"/dynamic_obj")==False:
        os.makedirs(scenev_resource_folder_path+"/dynamic_obj")
    return scenev_resource_folder_path